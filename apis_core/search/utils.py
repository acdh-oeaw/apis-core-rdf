import json

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
    return json.loads(serialization)[0]["fields"]
