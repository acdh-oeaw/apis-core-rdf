from django import template
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
from django.utils.html import format_html
from django_tables2.tables import table_factory

from apis_core.relations.tables import RelationTable
from apis_core.relations.models import Relation
from apis_core.relations import utils

register = template.Library()


@register.simple_tag
def relations_table(relationtype=None, instance=None, tocontenttype=None):
    """
    List all relations of type `relationtype` that go from `instance` to
    something with type `contenttype`.
    If no `tocontenttype` is passed, it lists all relations from and to
    instance.
    If no `relationtype` is passed, it lists all relations.
    """
    model = None
    existing_relations = list()

    if tocontenttype:
        model = tocontenttype.model_class()

    if relationtype:
        relation_types = [relationtype]
    else:
        # special case: when the contenttype is the same as the contenttype of
        # the instance, we don't want *all* the relations where the instance
        # occurs, but only those where it occurs together with another of its
        # type
        if instance and ContentType.objects.get_for_model(instance) == tocontenttype:
            relation_types = utils.relation_content_types(combination=(model, model))
        else:
            relation_types = utils.relation_content_types(any_model=model)

    for rel in relation_types:
        if instance:
            existing_relations.extend(
                list(
                    rel.model_class().objects.filter(Q(subj=instance) | Q(obj=instance))
                )
            )
        else:
            existing_relations.extend(list(rel.model_class().objects.all()))

    cssid = "table"
    if model:
        cssid += f"_{tocontenttype.name}"
    else:
        cssid += "_relations"
    attrs = {
        "class": "table table-hover table-striped table-condensed",
        "hx-swap-oob": "true",
        "id": cssid,
    }

    table = RelationTable
    if model:
        table = table_factory(model, RelationTable)
    return table(existing_relations, attrs=attrs)


@register.inclusion_tag("templatetags/relations_links.html")
def relations_links(instance=None, tocontenttype=None, htmx=False):
    """
    Provide a list of links to relation views; If `instance` is passed,
    it only links to relations where an `instance` type can be part of.
    If `contenttype` is passed, it links only to relations that can occur
    between the `instance` contenttype and the `contentttype`.
    """
    tomodel = None
    if tocontenttype:
        tomodel = tocontenttype.model_class()

    frommodel = None
    instancect = None
    if instance:
        frommodel = type(instance)
        instancect = ContentType.objects.get_for_model(instance)

    return {
        "relation_types": [
            (ct, ct.model_class())
            for ct in utils.relation_content_types(combination=(frommodel, tomodel))
        ],
        "relation_types_reverse": utils.relation_content_types(
            subj_model=tomodel, obj_model=frommodel
        ),
        "instance": instance,
        "instancect": instancect,
        "contenttype": tocontenttype,
        "htmx": htmx,
    }


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
def instance_can_be_related_to(instance: object) -> list[ContentType]:
    return contenttype_can_be_related_to(ContentType.objects.get_for_model(instance))


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


@register.simple_tag
def relations_css() -> str:
    """
    include a custom `relations.css` file
    """
    cssfile = static("relations.css")
    return format_html('<link rel="stylesheet" href="{}">', cssfile)
