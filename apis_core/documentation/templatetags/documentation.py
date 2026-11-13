from django import template
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apis_core.entities.templatetags.entities import get_entitymodels
from apis_core.relations.templatetags.relations import get_relationmodels


register = template.Library()


@register.inclusion_tag("documentation/templatetags/graph.html")
def entity_relation_model():
    return {
            "entities": get_entitymodels(),
            "relations": get_relationmodels()
    }

@register.filter
def escapecolon(value: str) -> str:
    return value.replace(":", "#58;")
