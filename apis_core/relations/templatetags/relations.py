from django import template
from django.contrib.contenttypes.models import ContentType

from apis_core.relations.models import Relation
from apis_core.relations import utils
from apis_core.relations.tables import GenericRelationsTable
from apis_core.generic.helpers import (
    module_paths,
    first_member_match,
)
register = template.Library()


@register.simple_tag
def relations_table(instance, to_content_type):
    relations = utils.relations_from_instance_to_contenttype(instance, to_content_type)

    table_modules = module_paths(to_content_type.model_class(), path="tables", suffix="RelationTable")
    table_class = first_member_match(table_modules, GenericRelationsTable)

    return table_class(relations, instance=instance)


@register.inclusion_tag("relations/partials/relations_links.html", takes_context=True)
def relations_links(context, target_content_type=None):
    """
    Provide a list of links to relation forms
    """
    obj = context.get("object", None)

    context["relation_types"] = utils.relation_content_types(combination=(type(obj), target_content_type.model_class()))
    context["source_content_type"] = ContentType.objects.get_for_model(obj)
    context["target_content_type"] = target_content_type
    return context


def contenttype_can_be_related_to(ct: ContentType) -> list[ContentType]:
    models = set()
    for rel in utils.relation_content_types(any_model=ct.model_class()):
        for x in rel.model_class().subj_list():
            models.add(x)
        for x in rel.model_class().obj_list():
            models.add(x)
    contenttypes = ContentType.objects.get_for_models(*models)
    models = sorted(contenttypes.items(), key=lambda item: item[1].name)
    return [item[1] for item in models]


@register.simple_tag
def instance_can_be_related_to(instance: object = None) -> list[ContentType]:
    if instance is not None:
        return contenttype_can_be_related_to(ContentType.objects.get_for_model(instance))
    return []


@register.simple_tag
def instance_is_related_to(instance: object) -> list[ContentType]:
    models = set()
    for rel in Relation.objects.filter(subj=instance).select_subclasses():
        for model in rel.obj_list():
            models.add(model)
    for rel in Relation.objects.filter(obj=instance).select_subclasses():
        for model in rel.subj_list():
            models.add(model)
    contenttypes = ContentType.objects.get_for_models(*models)
    models = sorted(contenttypes.items(), key=lambda item: item[1].name)
    return [item[1] for item in models]
