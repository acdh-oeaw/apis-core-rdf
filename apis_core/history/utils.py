from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django_tables2 import RequestConfig

from apis_core.utils.settings import get_entity_settings_by_modelname


def triple_sidebar_history(obj: object, request, detail=True):
    side_bar = []

    triples_related_all = obj.get_triples_for_version()
    if obj.version_tag is not None:
        triples_related_all = triples_related_all.filter(
            Q(version_tag=obj.version_tag)
            | Q(version_tag__contains=f"{obj.version_tag},")
        )
    content_type = ContentType.objects.get_for_model(obj.instance_type)
    if "apis_core.apis_relations" in settings.INSTALLED_APPS:
        from apis_core.apis_relations.tables import get_generic_triple_table
        from apis_core.apis_relations.utils import (
            get_content_types_with_allowed_relation_from,
        )

        for other_content_type in get_content_types_with_allowed_relation_from(
            content_type
        ):
            triples_related_by_entity = triples_related_all.filter(
                (
                    Q(subj__self_contenttype=other_content_type)
                    & Q(obj__pk=obj.instance.pk)
                )
                | (
                    Q(obj__self_contenttype=other_content_type)
                    & Q(subj__pk=obj.instance.pk)
                )
            )

            table_class = get_generic_triple_table(
                other_entity_class_name=other_content_type.model,
                entity_pk_self=obj.instance.pk,
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
