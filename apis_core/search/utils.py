import json
import unicodedata

from django.apps import apps
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from apis_core.search.serializers import SearchSerializer


def is_model_registered_for_search(model: models.Model) -> bool:
    config = getattr(model, "Config", {})
    return getattr(config, "index_for_search", False)


def get_models_registered_for_search() -> list[models.Model]:
    return list(filter(lambda x: is_model_registered_for_search(x), apps.get_models()))


def get_search_serialization_from_instance(instance) -> dict:
    if hasattr(instance, "search_serialization"):
        return instance.search_serialization()

    serializer = SearchSerializer()
    fields = getattr(instance.__class__.Config, "search_fields", None)
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
