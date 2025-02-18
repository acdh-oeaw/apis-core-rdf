from django import template
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from apis_core.core.templatetags.core import get_model_fields
from apis_core.generic.abc import GenericModel
from apis_core.generic.helpers import template_names_via_mro

register = template.Library()


@register.filter
def contenttype(model):
    return ContentType.objects.get_for_model(model)


@register.simple_tag
def modeldict(instance, fields=None, exclude=None):
    data = {}
    for f in get_model_fields(instance):
        if not getattr(f, "editable", False):
            continue
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        field = instance._meta.get_field(f.name)
        data[field] = instance._get_FIELD_display(field)
        if getattr(field, "remote_field", False):
            data[field] = getattr(instance, field.name)
        if getattr(field, "m2m_field_name", False):
            values = getattr(instance, field.name).all()
            data[field] = ", ".join([str(value) for value in values])
    return data


@register.simple_tag
def contenttypes(app_labels=None):
    if app_labels:
        app_labels = app_labels.split(",")
        return ContentType.objects.filter(app_label__in=app_labels)
    return ContentType.objects.all()


def is_genericmodel(content_type: ContentType):
    model_class = content_type.model_class()
    return model_class is not None and issubclass(model_class, GenericModel)


@register.simple_tag
def genericmodel_content_types():
    """
    Retrieve all models which inherit from GenericModel class
    and return their ContentType.
    """
    genericmodels = list(
        filter(
            lambda content_type: is_genericmodel(content_type),
            ContentType.objects.all(),
        )
    )
    return genericmodels


@register.simple_tag
def pure_genericmodel_content_types():
    """
    Retrieve all models which inherit from GenericModel class
    but are not Collections, Entities, Relations or History models
    """
    parents = []
    if apps.is_installed("apis_core.collections"):
        collections = apps.get_app_config("collections")
        parents.append(collections.models_module.SkosCollection)
        parents.append(collections.models_module.SkosCollectionContentObject)
    if apps.is_installed("apis_core.relations"):
        relations = apps.get_app_config("relations")
        parents.append(relations.models_module.Relation)
    if apps.is_installed("apis_core.history"):
        history = apps.get_app_config("history")
        parents.append(history.models_module.APISHistoryTableBase)
    if apps.is_installed("apis_core.apis_entities"):
        entities = apps.get_app_config("apis_entities")
        parents.append(entities.models_module.AbstractEntity)
    genericmodels = [
        ct
        for ct in set(genericmodel_content_types())
        if not issubclass(ct.model_class(), tuple(parents))
    ]
    return genericmodels


@register.filter
def get_attribute(obj, attribute):
    return getattr(obj, attribute, None)


@register.filter
def content_type_count(content_type):
    """
    Return the number of objects having a specific content type
    """
    return content_type.model_class().objects.count()


@register.simple_tag
def template_list(obj, suffix):
    return template_names_via_mro(type(obj), suffix)


@register.simple_tag(takes_context=True)
def any_view_permission(context, content_types):
    user = context.request.user
    return any(
        [user.has_perm(ct.model_class().get_view_permission()) for ct in content_types]
    )
