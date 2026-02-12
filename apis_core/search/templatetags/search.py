import re
from functools import cache

from django import template
from django.contrib.contenttypes.models import ContentType

from apis_core.search.utils import split_query_string_for_search

register = template.Library()


@register.filter(name="id_to_content_type")
@cache
def id_to_content_type(value):
    return ContentType.objects.get(pk=value)


def create_pattern_from_search_string(search_string: str) -> str:
    parts = split_query_string_for_search(search_string)
    pattern = "|".join(rf"{re.escape(part)}" for part in parts)
    return pattern


@register.simple_tag
def highlight_matches(data: dict, search_string: str) -> dict:
    data = {k: v for k, v in data.items() if v}
    pattern = create_pattern_from_search_string(search_string)
    result = {}
    for key, value in data.items():
        value = str(value)
        result[key] = {"orig": value}
        new_value = re.sub(pattern, r"<mark>\g<0></mark>", value, flags=re.IGNORECASE)
        if new_value != value:
            result[key]["match"] = new_value
    result = {key: value for key, value in result.items() if value.get("match")}
    return dict(result)


@register.filter
def highlight_matches_string(value: str, search_string: str) -> str:
    pattern = create_pattern_from_search_string(search_string)
    new_value = re.sub(pattern, r"<mark>\g<0></mark>", value, flags=re.IGNORECASE)
    return new_value
