from django import template
from django.conf import settings

from apis_core import __version__

register = template.Library()


@register.simple_tag
def shared_url():
    return getattr(settings, "SHARED_URL", "/static/")


@register.simple_tag
def page_range(paginator, number):
    return paginator.get_elided_page_range(number=number)


@register.filter
def opts(obj):
    return obj._meta


@register.filter
def model_meta(content_type, field):
    return getattr(content_type.model_class()._meta, field)


@register.simple_tag
def apis_version():
    return __version__


@register.simple_tag
def git_repository_url():
    return getattr(
        settings, "GIT_REPOSITORY_URL", "https://github.com/acdh-oeaw/apis-core-rdf/"
    )


@register.simple_tag
def get_model_fields(
    model, include_parents=True, include_hidden=False, exclude_parent_links=True
):
    """
    Return all fields from a model.
    This uses the Django built in `get_fields` method but also allows to exlude parent links.
    Parent links are the `_ptr` fields that point to a parent class.
    """
    fields = model._meta.get_fields(include_parents, include_hidden)
    if exclude_parent_links:
        parent_links = model._meta.parents.values()
        fields = [field for field in fields if field not in parent_links]
    return fields
