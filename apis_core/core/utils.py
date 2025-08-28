from itertools import chain

from django.db.models import Q

from apis_core.apis_entities.utils import get_entity_classes
from apis_core.generic.helpers import generate_search_filter
from apis_core.relations.models import Relation


def search(query: str, user: object):
    # search in entities:
    entities = get_entity_classes()
    res = []
    for entity in entities:
        if user.has_perm(entity.get_view_permission()):
            res.append(entity.objects.filter(generate_search_filter(entity, query)))

    entity_ids = [entity.pk for entity in chain(*res)]
    relations = Relation.objects.select_subclasses().filter(
        Q(subj_object_id__in=entity_ids) | Q(obj_object_id__in=entity_ids)
    )

    return chain(*res, relations)
