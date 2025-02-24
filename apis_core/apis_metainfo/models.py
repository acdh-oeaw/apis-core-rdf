from urllib.parse import urlsplit

from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from model_utils.managers import InheritanceManager

from apis_core.generic.abc import GenericModel
from apis_core.utils import rdf
from apis_core.utils import settings as apis_settings


class RootObject(GenericModel, models.Model):
    """
    The very root thing that can exist in a given ontology. Several classes inherit from it.
    By having one overarching super class we gain the advantage of unique identifiers.
    """

    objects = models.Manager()
    objects_inheritance = InheritanceManager()


# Uri model
# We use a custom UriManager, so we can override the queryset `get`
# method. This way we can normalize the uri field.


class UriQuerySet(models.query.QuerySet):
    def get(self, *args, **kwargs):
        if "uri" in kwargs:
            kwargs["uri"] = get_normalized_uri(kwargs["uri"])
        return super().get(*args, **kwargs)


class UriManager(models.Manager):
    def get_queryset(self):
        return UriQuerySet(self.model)


class Uri(GenericModel, models.Model):
    uri = models.URLField(blank=True, null=True, unique=True, max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    objects = UriManager()

    def __str__(self):
        return str(self.uri)

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self.uri = get_normalized_uri(self.uri)
        if self.uri and not hasattr(self, "content_object"):
            try:
                result = rdf.get_something_from_uri(self.uri)
                if model := result.getattr("model", False):
                    obj = model(**result.get("attributes", {}))
                    obj.save()
                    self.content_type = ContentType.objects.get_for_model(obj)
                    self.object_id = obj.id
                else:
                    raise ImproperlyConfigured(
                        f"{self.uri}: did not find matching rdf defintion"
                    )
            except Exception as e:
                raise ValidationError(f"{e}: {self.uri}")

    def internal(self) -> bool:
        my_netloc = urlsplit(self.uri).netloc
        return any(
            [my_netloc == urlsplit(uri).netloc for uri in apis_settings.internal_uris()]
        )
