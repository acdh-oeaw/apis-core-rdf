from django import template
from apis_core.apis_relations.tables import TempTripleDetailTable, TempTripleEditTable
from django.contrib.contenttypes.models import ContentType
from apis_core.utils.helpers import (
    get_classes_with_allowed_relation_from,
    triples_related,
)
from apis_core.generic.helpers import first_member_match, module_paths
from django_tables2.config import RequestConfig

register = template.Library()


@register.simple_tag(takes_context=True)
def triple_tables_related_detail(context: dict, instance: object):
    request = context["request"]
    tables = []

    table_class_paths = module_paths(
        instance._meta.model, path="tables", suffix="TempTripleDetailTable"
    )
    table_class = first_member_match(table_class_paths, TempTripleDetailTable)
    paginate = getattr(table_class, "table_pagination", {"per_page": 100})

    for related_type in get_classes_with_allowed_relation_from(
        instance._meta.verbose_name
    ):
        related_content_type = ContentType.objects.get_for_model(related_type)
        triples = triples_related(instance.pk, related_content_type)
        if triples:
            table = table_class(triples, instance, prefix=related_type.__name__)
            table = RequestConfig(request, paginate=paginate).configure(table)
            tables.append((related_content_type, table))
    return tables


@register.simple_tag(takes_context=True)
def triple_tables_related_edit(context: dict, instance: object):
    request = context["request"]
    tables = []

    table_class_paths = module_paths(
        instance._meta.model, path="tables", suffix="TempTripleEditTable"
    )
    table_class = first_member_match(table_class_paths, TempTripleEditTable)
    paginate = getattr(table_class, "table_pagination", {"per_page": 25})

    for related_type in get_classes_with_allowed_relation_from(
        instance._meta.verbose_name
    ):
        related_content_type = ContentType.objects.get_for_model(related_type)
        triples = triples_related(instance.pk, related_content_type)
        table = table_class(triples, instance, prefix=related_type.__name__)
        table = RequestConfig(request, paginate=paginate).configure(table)
        tables.append((related_content_type, table))
    return tables
