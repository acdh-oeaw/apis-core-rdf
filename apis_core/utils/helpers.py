import functools
import itertools
from typing import Type


from apis_core.apis_entities.models import TempEntityClass
from apis_core.apis_relations.models import Property


@functools.lru_cache
def get_classes_with_allowed_relation_from(
    entity_name: str,
) -> list[Type[TempEntityClass]]:
    """Returns a list of classes to which the given class may be related by a Property"""

    # Find all the properties where the entity is either subject or object
    properties_with_entity_as_subject = Property.objects.filter(
        subj_class__model=entity_name
    ).prefetch_related("obj_class")
    properties_with_entity_as_object = Property.objects.filter(
        obj_class__model=entity_name
    ).prefetch_related("subj_class")

    content_type_querysets = []

    # Where entity is subject, get all the object content_types
    for p in properties_with_entity_as_subject:
        objs = p.obj_class.all()
        content_type_querysets.append(objs)
    # Where entity is object, get all the subject content_types
    for p in properties_with_entity_as_object:
        subjs = p.subj_class.all()
        content_type_querysets.append(subjs)

    # Join querysets with itertools.chain, call set to make unique, and extract the model class
    return [
        content_type.model_class()
        for content_type in set(itertools.chain(*content_type_querysets))
    ]
