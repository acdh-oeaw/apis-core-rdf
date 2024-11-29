from urllib.parse import urlsplit

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from model_utils.managers import InheritanceManager

from apis_core.generic.abc import GenericModel
from apis_core.utils import rdf
from apis_core.utils import settings as apis_settings
from apis_core.utils.normalize import clean_uri


class RootObject(GenericModel, models.Model):
    """
    The very root thing that can exist in a given ontology. Several classes inherit from it.
    By having one overarching super class we gain the advantage of unique identifiers.
    """

    # self_contenttype: a foreign key to the respective contenttype comes in handy when querying for
    # triples where the subject's or object's contenttype must be respected (e.g. get all triples
    # where the subject is a Person)
    self_contenttype = models.ForeignKey(
        ContentType,
        on_delete=models.deletion.CASCADE,
        null=True,
        blank=True,
        editable=False,
    )
    objects = models.Manager()
    objects_inheritance = InheritanceManager()

    def save(self, *args, **kwargs):
        self.self_contenttype = ContentType.objects.get_for_model(self)
        super().save(*args, **kwargs)


class InheritanceForwardManyToOneDescriptor(ForwardManyToOneDescriptor):
    def get_queryset(self, **hints):
        return self.field.remote_field.model.objects_inheritance.db_manager(
            hints=hints
        ).select_subclasses()


class InheritanceForeignKey(models.ForeignKey):
    forward_related_accessor_class = InheritanceForwardManyToOneDescriptor


# Uri model
# We use a custom UriManager, so we can override the queryset `get`
# method. This way we can normalize the uri field.


class UriQuerySet(models.query.QuerySet):
    def get(self, *args, **kwargs):
        if "uri" in kwargs:
            kwargs["uri"] = clean_uri(kwargs["uri"])
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

    def get_web_object(self):
        result = {
            "relation_pk": self.pk,
            "relation_type": "uri",
            "related_root_object": self.content_object.name,
            "related_root_object_url": self.content_object.get_absolute_url(),
            "related_root_object_class_name": self.content_object.__class__.__name__.lower(),
            "uri": self.uri,
        }
        return result

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self.uri = clean_uri(self.uri)
        if self.uri and not hasattr(self, "content_object"):
            try:
                definition, attributes = rdf.get_definition_and_attributes_from_uri(
                    self.uri
                )
                if definition.getattr("model", False) and attributes:
                    app_label, model = definition.getattr("model").split(".", 1)
                    ct = ContentType.objects.get_by_natural_key(app_label, model)
                    obj = ct.model_class()(**attributes)
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
