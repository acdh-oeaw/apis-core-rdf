import functools

from django.contrib.contenttypes.models import ContentType

from apis_core.relations.models import Relation


def is_relation(ct: ContentType) -> bool:
    mc = ct.model_class()
    return (
        issubclass(mc, Relation)
        and hasattr(mc, "subj_model")
        and hasattr(mc, "obj_model")
    )


@functools.cache
def relation_content_types(
    subj_model=None, obj_model=None, any_model=None, combination=(None, None)
) -> set[ContentType]:
    allcts = list(
        filter(
            lambda contenttype: contenttype.model_class() is not None,
            ContentType.objects.all(),
        )
    )
    relationcts = list(filter(lambda contenttype: is_relation(contenttype), allcts))
    if subj_model is not None:
        relationcts = list(
            filter(
                lambda contenttype: subj_model
                is contenttype.model_class().subj_model_type(),
                relationcts,
            )
        )
    if obj_model is not None:
        relationcts = list(
            filter(
                lambda contenttype: obj_model
                is contenttype.model_class().obj_model_type(),
                relationcts,
            )
        )
    if any_model is not None:
        relationcts = list(
            filter(
                lambda contenttype: any_model
                is contenttype.model_class().obj_model_type()
                or any_model is contenttype.model_class().subj_model_type(),
                relationcts,
            )
        )
    if all(combination):
        left, right = combination
        rels = list(
            filter(
                lambda contenttype: right is contenttype.model_class().obj_model_type()
                and left is contenttype.model_class().subj_model_type(),
                relationcts,
            )
        )
        rels.extend(
            list(
                filter(
                    lambda contenttype: left
                    is contenttype.model_class().obj_model_type()
                    and right is contenttype.model_class().subj_model_type(),
                    relationcts,
                )
            )
        )
        relationcts = rels
    return set(relationcts)


def relation_match_target(relation, target: ContentType) -> bool:
    """
    test if a relation points to a target
    this function should not be cached, because the `forward` attribute
    is an annotation that does not seem to be part of the relation, so
    if cached, method could be called with another `forward` value and
    return the wrong result
    """
    if relation.forward and relation.obj_content_type == target:
        return True
    if not relation.forward and relation.subj_content_type == target:
        return True
    return False


@functools.cache
def get_all_relation_subj_and_obj() -> list[ContentType]:
    """
    Return the model classes of any model that is in some way
    connected to a relation - either as obj or as subj

    Returns:
    list[ContentType]: A list of unique ContentTypes for related models.
    """
    related_models = set()
    for rel in relation_content_types():
        related_models.add(rel.model_class().subj_model_type())
        related_models.add(rel.model_class().obj_model_type())
    return [ContentType.objects.get_for_model(item) for item in related_models]
