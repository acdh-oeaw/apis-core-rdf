import json
import unicodedata

from django.core.serializers.json import DjangoJSONEncoder

from .registry import search
from .serializers import SearchSerializer


def get_search_serialization_from_instance(instance) -> dict:
    options = search.get_options(instance.__class__)

    if hasattr(instance, "search_serialization"):
        return instance.search_serialization()

    serializer = SearchSerializer()
    fields = options.get("fields", None)
    serialization = serializer.serialize(
        [instance], fields=fields, cls=DjangoJSONEncoder
    )
    serialization = unicodedata.normalize("NFKD", serialization)
    return json.loads(serialization)[0]["fields"]


def split_query_string_for_search(query_str: str) -> list:
    query_str = unicodedata.normalize("NFKD", query_str)
    words = query_str.split()
    if len(words) > 1:
        words.insert(0, query_str)
    parts = list(dict.fromkeys(words))
    return parts
