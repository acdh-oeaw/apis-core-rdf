from django.conf import settings


def shared_url(request):
    shared_url = getattr(settings, "SHARED_URL", "/static/")
    return {"SHARED_URL": shared_url}
