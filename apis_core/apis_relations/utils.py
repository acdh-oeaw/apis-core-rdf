import itertools

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django_tables2 import RequestConfig

from apis_core.apis_relations.models import Property, TempTriple
from apis_core.apis_relations.tables import get_generic_triple_table
from apis_core.utils.settings import get_entity_settings_by_modelname


def get_content_types_with_allowed_relation_from(
    content_type: ContentType,
) -> list[ContentType]:
    """Returns a list of ContentTypes to which the given ContentTypes may be related by a Property"""

    # Find all the properties where the entity is either subject or object
    properties_with_entity_as_subject = Property.objects.filter(
        subj_class=content_type
    ).prefetch_related("obj_class")
    properties_with_entity_as_object = Property.objects.filter(
        obj_class=content_type
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
    return set(itertools.chain(*content_type_querysets))


def triple_sidebar(obj: object, request, detail=True):
    content_type = ContentType.objects.get_for_model(obj)
    side_bar = []

    triples_related_all = (
        TempTriple.objects_inheritance.filter(Q(subj__pk=obj.pk) | Q(obj__pk=obj.pk))
        .all()
        .select_subclasses()
    )

    for other_content_type in get_content_types_with_allowed_relation_from(
        content_type
    ):
        triples_related_by_entity = triples_related_all.filter(
            (Q(subj__self_contenttype=other_content_type) & Q(obj__pk=obj.pk))
            | (Q(obj__self_contenttype=other_content_type) & Q(subj__pk=obj.pk))
        )

        table_class = get_generic_triple_table(
            other_entity_class_name=other_content_type.model,
            entity_pk_self=obj.pk,
            detail=detail,
        )

        prefix = f"{other_content_type.model}"
        title_card = other_content_type.name
        tb_object = table_class(data=triples_related_by_entity, prefix=prefix)
        tb_object_open = request.GET.get(prefix + "page", None)
        entity_settings = get_entity_settings_by_modelname(content_type.model)
        per_page = entity_settings.get("relations_per_page", 10)
        RequestConfig(request, paginate={"per_page": per_page}).configure(tb_object)
        tab_id = f"triple_form_{content_type.model}_to_{other_content_type.model}"
        side_bar.append(
            (
                title_card,
                tb_object,
                tab_id,
                tb_object_open,
            )
        )
    return side_bar
