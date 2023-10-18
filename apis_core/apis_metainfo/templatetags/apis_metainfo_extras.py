from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.inclusion_tag("apis_metainfo/tags/class_definition.html", takes_context=True)
def class_definition(context):
    values = {}
    try:
        values["class_name"] = context["class_name"]
        values["docstring"] = context["docstring"]
    except Exception as e:
        print(e)
        pass
    return values
