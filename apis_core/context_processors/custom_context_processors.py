from django.conf import settings


def list_apis_settings(request):
    """adds the custom settings to the templates"""
    res = {
        "additional_functions": getattr(settings, "APIS_COMPONENTS", []),
        "request": request,
        "basetemplate": getattr(settings, "BASE_TEMPLATE", "base.html"),
    }
    if "apis_bibsonomy" in settings.INSTALLED_APPS:
        res["bibsonomy_active"] = True
    else:
        res["bibsonomy_active"] = False
    return res
