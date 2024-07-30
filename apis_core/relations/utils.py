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
                lambda contenttype: subj_model in contenttype.model_class().subj_list(),
                relationcts,
            )
        )
    if obj_model is not None:
        relationcts = list(
            filter(
                lambda contenttype: obj_model in contenttype.model_class().obj_list(),
                relationcts,
            )
        )
    if any_model is not None:
        relationcts = list(
            filter(
                lambda contenttype: any_model in contenttype.model_class().obj_list()
                or any_model in contenttype.model_class().subj_list(),
                relationcts,
            )
        )
    if all(combination):
        left, right = combination
        rels = list(
            filter(
                lambda contenttype: right in contenttype.model_class().obj_list()
                and left in contenttype.model_class().subj_list(),
                relationcts,
            )
        )
        rels.extend(
            list(
                filter(
                    lambda contenttype: left in contenttype.model_class().obj_list()
                    and right in contenttype.model_class().subj_list(),
                    relationcts,
                )
            )
        )
        relationcts = rels
    return set(relationcts)


@functools.cache
def relation_match_target(relation, target: ContentType) -> bool:
    if relation.forward and relation.obj_content_type == target:
        return True
    if not relation.forward and relation.subj_content_type == target:
        return True
    return False
