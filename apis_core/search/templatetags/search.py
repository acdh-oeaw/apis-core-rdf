import functools
import re

from django import template
from django.contrib.contenttypes.models import ContentType

from apis_core.search.utils import split_query_string_for_search

register = template.Library()


@register.filter
@functools.cache
def id_to_content_type(value):
    return ContentType.objects.get(pk=value)


@register.simple_tag
@functools.cache
def get_model_field_by_content_type_id_and_name(
    content_type_id, field_name: str
) -> str:
    model = ContentType.objects.get(pk=content_type_id).model_class()
    return model._meta.get_field(field_name)


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
            result[key]["match"] = []
            for match in re.finditer(r"<mark>.*?</mark>", new_value):
                m_start = max(match.start() - 10, 0)
                m_end = min(match.end() + 10, len(new_value))
                extracted_string = new_value[m_start:m_end]
                if m_start != 0:
                    extracted_string = "..." + extracted_string
                if m_end != len(new_value):
                    extracted_string += "..."
                result[key]["match"].append(extracted_string)
    result = {key: value for key, value in result.items() if value.get("match")}
    return dict(result)


@register.filter
def highlight_matches_string(value: str, search_string: str) -> str:
    pattern = create_pattern_from_search_string(search_string)
    new_value = re.sub(pattern, r"<mark>\g<0></mark>", value, flags=re.IGNORECASE)
    return new_value
