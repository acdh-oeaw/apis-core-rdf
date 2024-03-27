from apis_core.apis_relations.tables import get_generic_triple_table
from apis_core.utils.helpers import get_classes_with_allowed_relation_from
from apis_core.utils.settings import get_entity_settings_by_modelname
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django_tables2 import RequestConfig


def triple_sidebar_history(pk: int, entity_name: str, request, detail=True):
    side_bar = []
    entity_name = entity_name.replace("version", "")

    historical_entity = (
        ContentType.objects.get(model=entity_name)
        .model_class()
        .history.get(history_id=pk)
    )
    triples_related_all = historical_entity.get_triples_for_version()
    if historical_entity.version_tag is not None:
        triples_related_all = triples_related_all.filter(
            Q(version_tag=historical_entity.version_tag)
            | Q(version_tag__contains=f"{historical_entity.version_tag},")
        )
    pk = historical_entity.instance.pk

    for entity_class in get_classes_with_allowed_relation_from(entity_name):
        entity_content_type = ContentType.objects.get_for_model(entity_class)

        other_entity_class_name = entity_class.__name__.lower()

        triples_related_by_entity = triples_related_all.filter(
            (Q(subj__self_contenttype=entity_content_type) & Q(obj__pk=pk))
            | (Q(obj__self_contenttype=entity_content_type) & Q(subj__pk=pk))
        )

        table_class = get_generic_triple_table(
            other_entity_class_name=other_entity_class_name,
            entity_pk_self=pk,
            detail=detail,
        )

        prefix = f"{other_entity_class_name}"
        title_card = prefix
        tb_object = table_class(data=triples_related_by_entity, prefix=prefix)
        tb_object_open = request.GET.get(prefix + "page", None)
        entity_settings = get_entity_settings_by_modelname(entity_class.__name__)
        per_page = entity_settings.get("relations_per_page", 10)
        RequestConfig(request, paginate={"per_page": per_page}).configure(tb_object)
        tab_id = f"triple_form_{entity_name}_to_{other_entity_class_name}"
        side_bar.append(
            (
                title_card,
                tb_object,
                tab_id,
                tb_object_open,
            )
        )
    return side_bar
