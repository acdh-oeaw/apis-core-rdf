from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured

from apis_core.apis_metainfo.models import Uri
from apis_core.utils.helpers import get_importer_for_model


def create_object_from_uri(uri: str, model: object, raise_on_fail=False) -> object:
    if uri.startswith("http"):
        try:
            uri = Uri.objects.get(uri=uri)
            return uri.content_object
        except Uri.DoesNotExist:
            Importer = get_importer_for_model(model)
            importer = Importer(uri, model)
            instance = importer.create_instance()
            content_type = ContentType.objects.get_for_model(instance)
            uri = Uri.objects.create(
                uri=importer.get_uri,
                content_type=content_type,
                object_id=instance.id,
            )
            return instance
    if raise_on_fail:
        content_type = ContentType.objects.get_for_model(model)
        raise ImproperlyConfigured(
            f'Could not create {content_type.name} from string "{uri}"'
        )
    return False
