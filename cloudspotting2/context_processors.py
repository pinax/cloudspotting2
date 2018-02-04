from django.conf import settings as django_settings
from django.contrib.sites.models import Site


def pinax_apps_filter(app):
    return app.startswith("pinax.") or app in ["account", "mailer"]


def transform_package_name(name):
    if name.startswith("pinax."):
        return name.replace(".", "-")
    elif name == "account":
        return "django-user-accounts"
    elif name == "mailer":
        return "django-mailer"
    else:
        return name


def package_names(names):
    """
    Returns list of names sorted by core_apps first, then alphabetical order
    """
    core_apps = ["pinax.templates", "account", "pinax.eventlog", "pinax.webanalytics"]
    apps = []
    for x in names:
        if x in core_apps:
            index = core_apps.index(x)
        else:
            index = 55
        # add to decorated list
        apps.append((index, transform_package_name(x)))

    # sort apps
    apps.sort()

    # undecorate
    return [x[1] for x in apps]


def settings(request):
    ctx = {
        "ADMIN_URL": django_settings.ADMIN_URL,
        "CONTACT_EMAIL": django_settings.CONTACT_EMAIL,

        "pinax_notifications_installed": "pinax.notifications" in django_settings.INSTALLED_APPS,
        "pinax_stripe_installed": "pinax.stripe" in django_settings.INSTALLED_APPS,

        "pinax_apps": package_names(filter(pinax_apps_filter, django_settings.INSTALLED_APPS))
    }

    if Site._meta.installed:
        site = Site.objects.get_current(request)
        ctx.update({
            "SITE_NAME": site.name,
            "SITE_DOMAIN": site.domain
        })

    return ctx
