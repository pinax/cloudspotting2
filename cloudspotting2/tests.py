from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.urls import reverse

from pinax.announcements.models import Announcement
from pinax.images.models import ImageSet
from pinax.invitations.models import InvitationStat, JoinInvitation
from pinax.likes.models import Like
from test_plus.test import TestCase

from .models import CloudSpotting


class TestViews(TestCase):

    def setUp(self):
        super(TestViews, self).setUp()
        self.user = self.make_user("cirrus")
        self.cloud_type = "cumulonimbus"
        self.spotting = CloudSpotting.objects.create(
            cloud_type=self.cloud_type,
            user=self.user,
            image_set=ImageSet.objects.create(created_by=self.user)
        )

    def test_list(self):
        """
        Ensure list contains all CloudSpotting collections.
        """
        with self.login(self.user):
            self.get("cloudspotting_list")
            self.response_200()
            object_list = self.get_context("object_list")
            self.assertEqual(object_list[0], self.spotting)

    def test_invalid_detail(self):
        """
        Ensure GET with invalid CloudSpotting PK fails.
        """
        with self.login(self.user):
            self.get("cloudspotting_detail", pk=555)
            self.response_404()

    def test_detail(self):
        """
        Ensure GET with valid CloudSpotting PK succeeds.
        """
        with self.login(self.user):
            self.get("cloudspotting_detail", pk=self.spotting.pk)
            self.response_200()
            context_object = self.get_context("cloudspotting")
            self.assertEqual(context_object, self.spotting)

    def test_create(self):
        """
        Ensure successful CloudSpotting creation.
        """
        cloud_type = "nimbus"
        post_args = dict(
            cloud_type=cloud_type
        )
        with self.login(self.user):
            self.post("cloudspotting_create", data=post_args, follow=True)
            self.response_200()
            self.assertTrue(
                next(iter(CloudSpotting.objects.filter(cloud_type=cloud_type)), None)
            )

    def test_delete(self):
        """
        Ensure CloudSpotting is really deleted.
        """
        with self.login(self.user):
            self.post("cloudspotting_delete", pk=self.spotting.pk, follow=True)
            self.response_200()
            self.assertFalse(
                next(iter(CloudSpotting.objects.filter(cloud_type=self.spotting.cloud_type)), None)
            )


class TestAnnouncements(TestCase):

    def setUp(self):
        super(TestAnnouncements, self).setUp()
        self.user = self.make_user("cirrus")
        self.staff = self.make_user("staff")
        # Make this user "staff" for "can_manage" permission.
        self.staff.is_staff = True
        self.staff.save()
        self.assertTrue(self.staff.has_perm("announcements.can_manage"))

    def test_announcements(self):
        """
        Ensure page showing announcements contains new announcement.
        """
        title = "Election Results"
        announcement = Announcement.objects.create(
            title=title,
            content="some results",
            creator=self.staff,
            site_wide=True
        )
        announcement.save()
        with self.login(self.user):
            response = self.get("cloudspotting_list")
            self.response_200()
            self.assertIn(bytes(title, encoding="utf-8"), response.content)


class TestInvitationsNotifications(TestCase):

    fixtures = ["noticetypes.json"]

    def test_invitation_accepted(self):
        """Verify inviter whose invitee accepts invitation is notified"""
        inviter = self.make_user("inviter")
        InvitationStat.add_invites(2)

        invitee_email = "invitee@example.com"
        with self.login(inviter):
            post_data = {"email_address": invitee_email}
            self.post("pinax_invitations:invite", data=post_data)
            self.response_200()

        invitation = JoinInvitation.objects.first()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(invitee_email, mail.outbox[0].to)
        mail.outbox.clear()

        # Accept the invitation
        invitee_username = "invitee"
        post_data = dict(
            username=invitee_username,
            password="notasecret",
            password_confirm="notasecret",
            email=invitee_email,
        )

        url = reverse("account_signup")
        self.post(url + f"?code={invitation.signup_code.code}", data=post_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(inviter.email, mail.outbox[0].to)
        self.assertIn(
            f"User \"{invitee_username}\" ({invitee_email}) joined this site at your invitation",
            mail.outbox[0].body
        )


class TestLikesNotifications(TestCase):
    """
    Integration tests proving if user posts to "Like" view,
    owner of the liked collection is notified.
    """
    fixtures = ["noticetypes.json"]

    def test_image_liked(self):
        """Verify that collection owner is notified when a user "likes" the collection"""
        owner = self.make_user("owner")
        cloud_type = "cumulonimbus"
        spotting = CloudSpotting.objects.create(
            cloud_type=cloud_type,
            user=owner,
            image_set=ImageSet.objects.create(created_by=owner)
        )
        content_type = ContentType.objects.get(model="cloudspotting")

        liker = self.make_user("liker")
        with self.login(liker):
            self.assertFalse(Like.objects.filter(receiver_content_type=content_type, receiver_object_id=spotting.pk).exists())
            self.post("pinax_likes:like_toggle", content_type.pk, spotting.pk)
            self.response_302()
            self.assertTrue(Like.objects.filter(receiver_content_type=content_type, receiver_object_id=spotting.pk).exists())

            self.assertEqual(len(mail.outbox), 1)
            self.assertIn(owner.email, mail.outbox[0].to)
            self.assertIn(
                f"User \"{liker.username}\" liked your \"{spotting.cloud_type}\" collection",
                mail.outbox[0].body
            )
