import functools
import re

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import NoReverseMatch, reverse

from apis_core.apis_metainfo.models import RootObject, Uri

NEXT_PREV = getattr(settings, "APIS_NEXT_PREV", True)


class AbstractEntity(RootObject):
    """
    Abstract super class which encapsulates common logic between the
    different entity kinds and provides various methods relating to either
    all or one specific entity kind.

    Most of the class methods are designed to be used in the subclass as they
    are considering contexts which depend on the subclass entity type.
    So they are to be understood in that dynamic context.
    """

    class Meta:
        abstract = True

    @classmethod
    def get_or_create_uri(cls, uri):
        uri = str(uri)
        try:
            if re.match(r"^[0-9]*$", uri):
                p = cls.objects.get(pk=uri)
            else:
                p = cls.objects.get(uri__uri=uri)
            return p
        except Exception as e:
            print("Found no object corresponding to given uri." + e)
            return False

    # TODO
    @classmethod
    def get_entity_list_filter(cls):
        return None

    @functools.cached_property
    def get_prev_id(self):
        if NEXT_PREV:
            prev_instance = (
                type(self)
                .objects.filter(id__lt=self.id)
                .order_by("-id")
                .only("id")
                .first()
            )
            if prev_instance is not None:
                return prev_instance.id
        return False

    @functools.cached_property
    def get_next_id(self):
        if NEXT_PREV:
            next_instance = (
                type(self)
                .objects.filter(id__gt=self.id)
                .order_by("id")
                .only("id")
                .first()
            )
            if next_instance is not None:
                return next_instance.id
        return False

    def get_duplicate_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_duplicate_view",
            kwargs={"contenttype": entity, "pk": self.id},
        )

    def merge_start_date_written(self, other):
        self.start_date_written = self.start_date_written or other.start_date_written

    def merge_end_date_written(self, other):
        self.end_date_written = self.end_date_written or other.end_date_written


@receiver(post_save, dispatch_uid="create_default_uri")
def create_default_uri(sender, instance, created, raw, using, update_fields, **kwargs):
    # disable the handler during fixture loading
    if raw:
        return
    create_default_uri = getattr(settings, "CREATE_DEFAULT_URI", True)
    skip_default_uri = getattr(instance, "skip_default_uri", False)
    if create_default_uri and not skip_default_uri:
        if isinstance(instance, AbstractEntity) and created:
            base = getattr(settings, "APIS_BASE_URI", "https://example.org").strip("/")
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
