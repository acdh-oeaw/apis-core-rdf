from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from .models import SearchEntry


def reindex_model_instance(instance):
    content_type = ContentType.objects.get_for_model(instance)
    defaults = {
        "title": str(instance),
        "content": serialize("json", [instance], cls=DjangoJSONEncoder),
    }
    s, c = SearchEntry.objects.update_or_create(
        content_type=content_type, object_id=instance.pk, defaults=defaults
    )
