from apis_core.apis_entities.models import TempEntityClass
from django.contrib.contenttypes.models import ContentType

def get_all_entity_content_types():
    all_cts = ContentType.objects.all()
    # sometimes there are stale contenttypes where the
    # model_class is None - we filter those out:
    all_cts = [ct for ct in all_cts if ct.model_class()]
    return [ct for ct in all_cts if issubclass(ct.model_class(), TempEntityClass) and ct.model_class() != TempEntityClass]

def get_all_entity_classes():
    return [ct.model_class() for ct in get_all_entity_content_types()]

def get_entity_class_by_shortname(shortname: str):
    shortname = shortname.lower()
    content_types = get_all_entity_content_types()
    content_types = list(filter(lambda n: n.model == shortname, content_types))
    if content_types:
        return content_types[0].model_class()
    raise Exception("Could not find entity class of name:", shortname)
