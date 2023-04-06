from operator import itemgetter

from django.conf import settings

from apis_core.helper_functions import caching


def list_entities(request):
    """
    Retrieve all models which inherit from AbstractEntity class
    and make information about them available on the frontend.

    :return a dictionary of context items
    """
    entities_classes = caching.get_all_entity_classes() or []
    # create (uri, label) tuples for entities for use in templates
    entities_links = [
        (e.__name__.lower(), e._meta.verbose_name.title()) for e in entities_classes
    ]
    entities_links.sort(key=itemgetter(1))

    return {"entities_links": entities_links, "request": request}


def list_relations(request):
    return {"relations_list": ["property", "triple"], "request": request}


def list_apis_settings(request):
    """adds the custom settings to the templates"""
    res = {
        "additional_functions": getattr(settings, "APIS_COMPONENTS", []),
        "request": request,
    }
    if "apis_highlighter" in settings.INSTALLED_APPS:
        res["highlighter_active"] = True
    else:
        res["highlighter_active"] = False
    if "apis_bibsonomy" in settings.INSTALLED_APPS:
        res["bibsonomy_active"] = True
    else:
        res["bibsonomy_active"] = False
    return res
