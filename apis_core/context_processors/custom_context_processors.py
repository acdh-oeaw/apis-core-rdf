import inspect
import sys

from django.conf import settings


def add_entities(request):
    """
    Retrieve all models which inherit from AbstractEntity class
    and make information about them available on the frontend.

    :return a dictionary of context items
    """
    from apis_core.apis_entities.models import AbstractEntity

    entities_classes = AbstractEntity.get_all_entity_classes() or []
    # create (uri, label) tuples for entities for use in templates
    entities_links = [(e.__name__.lower(), e._meta.verbose_name_plural.title()) for e in entities_classes]
    entities_uris = [u[0] for u in entities_links]  # TODO kk for compatibility, see below

    res = {
        'entities_list': entities_uris,  # TODO kk keep for compatibility; remove when not used in templates anymore
        'entities_classes': entities_classes,
        'entities_links': entities_links,
        'request': request
    }
    return res


def add_relations(request):
    relations_list = []
    for name, obj in inspect.getmembers(
        sys.modules['apis_core.apis_relations.models'], inspect.isclass
    ):
        if obj.__module__ == 'apis_core.apis_relations.models' and name not in ["AbstractRelation", "AnnotationRelationLinkManager", "ent_class", "BaseRelationManager", "RelationPublishedQueryset"]:
            relations_list.append(str(name).lower())
    res = {
        'relations_list': relations_list,
        'request': request
    }
    return res


def add_apis_settings(request):
    """adds the custom settings to the templates"""
    res = {
        'additional_functions': getattr(settings, "APIS_COMPONENTS", []),
        'request': request
    }
    if 'apis_highlighter' in settings.INSTALLED_APPS:
        res['highlighter_active'] = True
    else:
        res['highlighter_active'] = False
    if 'apis_bibsonomy' in settings.INSTALLED_APPS:
        res['bibsonomy_active'] = True
    else:
        res['bibsonomy_active'] = False
    return res
