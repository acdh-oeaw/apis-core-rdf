from django import template

from apis_core.uris.models import Uri

register = template.Library()


@register.simple_tag
def instance_uris(instance):
    """
    Return all URIs that point to a specific model instance
    """
    return Uri.objects.get_for_instance(instance)


@register.inclusion_tag("uris/uri_list.html", takes_context=True)
def uri_list(context, instance):
    uris = Uri.objects.get_for_instance(instance)
    app_label, model = instance._meta.label_lower.split(".")
    context["uris"] = uris
    context["object"] = instance
    context["app_label"] = app_label
    context["model"] = model
    return context
