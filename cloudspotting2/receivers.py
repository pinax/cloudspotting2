from django.dispatch import receiver

from account.signals import (
    password_changed,
    user_logged_in,
    user_login_attempt,
    user_sign_up_attempt,
    user_signed_up,
)
from pinax.eventlog.models import log
from pinax.invitations.signals import invite_accepted, joined_independently
from pinax.likes.signals import object_liked
from pinax.notifications.models import send


@receiver(user_logged_in)
def handle_user_logged_in(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_LOGGED_IN",
        extra={}
    )


@receiver(password_changed)
def handle_password_changed(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="PASSWORD_CHANGED",
        extra={}
    )


@receiver(user_login_attempt)
def handle_user_login_attempt(sender, **kwargs):
    log(
        user=None,
        action="LOGIN_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_sign_up_attempt)
def handle_user_sign_up_attempt(sender, **kwargs):
    log(
        user=None,
        action="SIGNUP_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "email": kwargs.get("email"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_SIGNED_UP",
        extra={}
    )


@receiver(invite_accepted)
def handle_invite_accepted(sender, **kwargs):
    invitation = kwargs.get("invitation")
    log(
        user=invitation.to_user,
        action="INVITE_ACCEPTED",
        extra={}
    )
    send(
        [invitation.from_user],
        "invite_accepted",
        extra_context={"joiner": invitation.to_user.username, "email": invitation.to_user.email}
    )


@receiver(joined_independently)
def handle_joined_independently(sender, **kwargs):
    invitation = kwargs.get("invitation")
    log(
        user=invitation.to_user,
        action="JOINED_INDEPENDENTLY",
        extra={}
    )
    send(
        [invitation.from_user],
        "joined_independently",
        extra_context={"joiner": invitation.to_user.username}
    )


@receiver(object_liked)
def handle_object_liked(sender, **kwargs):
    like = kwargs.get("like")
    liker = like.sender
    cloudspotting = like.receiver
    log(
        user=liker,
        action="LIKED_CLOUDSPOTTING",
        extra={
            "pk": cloudspotting.pk,
        }
    )
    send(
        [cloudspotting.user],
        "cloudspotting_liked",
        extra_context={"cloud_type": cloudspotting.cloud_type, "liker": liker.username}
    )
