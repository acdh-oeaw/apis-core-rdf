import re
from collections import defaultdict
from functools import cache

from django import template
from django.contrib.contenttypes.models import ContentType

from apis_core.search.utils import split_query_string_for_search

register = template.Library()


@register.filter(name="id_to_content_type")
@cache
def id_to_content_type(value):
    return ContentType.objects.get(pk=value)


@register.simple_tag(name="highlight_matches")
def highlight_matches(data: dict, search_string: str) -> dict:
    data = {k: v for k, v in data.items() if v}
    parts = split_query_string_for_search(search_string)
    result = defaultdict(list)
    print(parts)
    for key, value in data.items():
        for part in parts:
            value = str(value)
            print(value)
            for match in re.finditer(part, value, re.IGNORECASE):
                print(match)
                matched_word = match.group(0)
                start = max(0, match.start() - 10)
                end = match.end() + 10
                matched_window = value[start:end].replace(
                    matched_word, f"<span class='match'>{matched_word}</span>"
                )
                result[key].append(f"...{matched_window}...")
    return dict(result)


@register.filter
def highlight_matches_string(value: str, search_string: str) -> str:
    parts = split_query_string_for_search(search_string)
    for part in parts:
        for match in re.finditer(part, value, re.IGNORECASE):
            matched_word = match.group(0)
            value = value.replace(
                matched_word, f"<span class='match'>{matched_word}</span>"
            )
    return value
