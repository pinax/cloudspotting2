from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("ajax/images/", include("pinax.images.urls", namespace="pinax_images")),
    path("announcements/", include("pinax.announcements.urls", namespace="pinax_announcements")),
    path("invitations/", include("pinax.invitations.urls", namespace="pinax_invitations")),
    path("likes/", include("pinax.likes.urls", namespace="pinax_likes")),
    path("messages/", include("pinax.messages.urls", namespace="pinax_messages")),
    path("notifications/", include("pinax.notifications.urls", namespace="pinax_notifications")),

    path("cloudspotting/", views.CloudSpottingListView.as_view(), name="cloudspotting_list"),
    path("cloudspotting/create/", views.CloudSpottingCreateView.as_view(), name="cloudspotting_create"),
    path("cloudspotting/<int:pk>/", views.CloudSpottingDetailView.as_view(), name="cloudspotting_detail"),
    path("cloudspotting/<int:pk>/update/", views.CloudSpottingUpdateView.as_view(), name="cloudspotting_update"),
    path("cloudspotting/<int:pk>/delete/", views.CloudSpottingDeleteView.as_view(), name="cloudspotting_delete"),
    path("invite/", TemplateView.as_view(template_name="cloudspotting2/invites.html"), name="invites"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
