import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import NoReverseMatch, reverse

from apis_core.apis_entities.models import AbstractEntity
from apis_core.apis_metainfo.models import Uri
from apis_core.utils.settings import apis_base_uri

logger = logging.getLogger(__name__)


@receiver(post_delete)
def remove_stale_uris(sender, instance, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    if isinstance(instance.pk, int):
        uris = Uri.objects.filter(content_type=content_type, object_id=instance.pk)
        for uri in uris:
            logger.info(
                "Deleting uri %s as a result of deleting %s", repr(uri), repr(instance)
            )
            uri.delete()


@receiver(post_save, dispatch_uid="create_default_uri")
def create_default_uri(sender, instance, created, raw, using, update_fields, **kwargs):
    # disable the handler during fixture loading
    if raw:
        return
    create_default_uri = getattr(settings, "CREATE_DEFAULT_URI", True)
    skip_default_uri = getattr(instance, "skip_default_uri", False)
    if create_default_uri and not skip_default_uri:
        if isinstance(instance, AbstractEntity) and created:
            base = apis_base_uri().strip("/")
            try:
                route = reverse("GetEntityGenericRoot", kwargs={"pk": instance.pk})
            except NoReverseMatch:
                route = reverse(
                    "apis_core:GetEntityGeneric", kwargs={"pk": instance.pk}
                )
            uri = f"{base}{route}"
            content_type = ContentType.objects.get_for_model(instance)
            Uri.objects.create(
                uri=uri,
                content_type=content_type,
                object_id=instance.id,
            )
