from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Case, Q, Value, When

from apis_core.generic.helpers import first_member_match, module_paths, mro_paths
from apis_core.relations.models import Relation
from apis_core.relations.tables import RelationsListTable
from apis_core.relations.utils import relation_content_types, relation_match_target

register = template.Library()


@register.simple_tag
def possible_relation_types_from(obj) -> list[ContentType]:
    return relation_content_types(any_model=type(obj))


@register.simple_tag
def get_relation_targets_from(obj) -> list[ContentType]:
    relations = relation_content_types(any_model=type(obj))
    types = set()
    for model in [relation.model_class() for relation in relations]:
        if type(obj) in model.obj_list():
            types.update(model.subj_list())
        if type(obj) in model.subj_list():
            types.update(model.obj_list())
    return sorted(
        list(map(ContentType.objects.get_for_model, types)), key=lambda x: x.name
    )


@register.simple_tag
def relations_from(from_obj, relation_type: ContentType = None):
    from_content_type = ContentType.objects.get_for_model(from_obj)
    relation = Relation
    if relation_type is not None:
        relation = relation_type.model_class()

    relations = (
        relation.objects.filter(
            Q(subj_content_type=from_content_type, subj_object_id=from_obj.id)
            | Q(obj_content_type=from_content_type, obj_object_id=from_obj.id)
        )
        .annotate(
            forward=Case(
                When(
                    subj_content_type=from_content_type,
                    subj_object_id=from_obj.id,
                    then=Value(True),
                ),
                default=Value(False),
            )
        )
        .select_subclasses()
    )
    return relations


@register.simple_tag(takes_context=True)
def relations_list_table(context, relations, target=None):
    suffixes = ["RelationsTable"]
    if target:
        suffixes.extend(
            f"{module[-1]}RelationsTable" for module in mro_paths(target.model_class())
        )
    table_modules = ()
    for suffix in suffixes:
        table_modules += module_paths(
            type(context["object"]), path="tables", suffix=suffix
        )
    table_class = first_member_match(table_modules, RelationsListTable)
    if target:
        relations = [
            relation
            for relation in relations
            if relation_match_target(relation, target)
        ]
    return table_class(relations, request=context["request"])


@register.simple_tag
def relations_verbose_name_listview_url():
    """
    Return all relations verbose names together with their list uri, sorted in alphabetical order
    USED BY:
    * `apis_core/relations/templates/base.html` (to extend the default `base.html`)
    """
    relation_classes = [relation.model_class() for relation in relation_content_types()]
    ret = {
        relation._meta.verbose_name: relation.get_listview_url()
        for relation in relation_classes
    }
    return sorted(ret.items())
