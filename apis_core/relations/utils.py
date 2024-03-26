import functools
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from apis_core.relations.models import Relation


def relations_from_instance_to_contenttype(instance, contenttype):
    model = contenttype.model_class()

    # special case: when the contenttype is the same as the contenttype of
    # the instance, we don't want *all* the relations where the instance
    # occurs, but only those where it occurs together with another of its
    # type
    if ContentType.objects.get_for_model(instance) == contenttype:
        relation_types = relation_content_types(combination=(model, model))
    else:
        relation_types = relation_content_types(any_model=model)

    relations = list()
    for rel in relation_types:
        rels = list(rel.model_class().objects.filter(Q(subj=instance, obj__self_contenttype=contenttype) | Q(obj=instance, subj__self_contenttype=contenttype)))
        relations.extend(rels)

    return relations


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
):
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
                lambda contenttype: contenttype.model_class().is_subj(subj_model),
                relationcts,
            )
        )
    if obj_model is not None:
        relationcts = list(
            filter(
                lambda contenttype: contenttype.model_class().is_obj(obj_model),
                relationcts,
            )
        )
    if any_model is not None:
        relationcts = list(
            filter(
                lambda contenttype: contenttype.model_class().is_obj(any_model)
                or contenttype.model_class().is_subj(any_model),
                relationcts,
            )
        )
    if all(combination):
        left, right = combination
        rels = list(
            filter(
                lambda contenttype: contenttype.model_class().is_obj(right)
                and contenttype.model_class().is_subj(left),
                relationcts,
            )
        )
        rels.extend(
            list(
                filter(
                    lambda contenttype: contenttype.model_class().is_obj(left)
                    and contenttype.model_class().is_subj(right),
                    relationcts,
                )
            )
        )
        relationcts = rels
    return set(relationcts)
