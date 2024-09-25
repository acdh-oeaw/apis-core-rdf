import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.forms import model_to_dict
from model_utils.managers import InheritanceManager

from apis_core.apis_metainfo import signals
from apis_core.generic.abc import GenericModel
from apis_core.utils import rdf
from apis_core.utils.normalize import clean_uri

logger = logging.getLogger(__name__)


NEXT_PREV = getattr(settings, "APIS_NEXT_PREV", True)


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

    def duplicate(self):
        origin = self.__class__
        signals.pre_duplicate.send(sender=origin, instance=self)
        # usually, copying instances would work like
        # https://docs.djangoproject.com/en/4.2/topics/db/queries/#copying-model-instances
        # but we are working with abstract classes,
        # so we have to do it by hand  using model_to_dict:(
        objdict = model_to_dict(self)

        # remove unique fields from dict representation
        unique_fields = [field for field in self._meta.fields if field.unique]
        for field in unique_fields:
            logger.info(f"Duplicating {self}: ignoring unique field {field.name}")
            objdict.pop(field.name, None)

        # remove related fields from dict representation
        related_fields = [
            field for field in self._meta.get_fields() if field.is_relation
        ]
        for field in related_fields:
            objdict.pop(field.name, None)

        newobj = type(self).objects.create(**objdict)

        for field in related_fields:
            # we are not using `isinstance` because we want to
            # differentiate between different levels of inheritance
            if type(field) is ForeignKey:
                setattr(newobj, field.name, getattr(self, field.name))
            if type(field) is ManyToManyField:
                objfield = getattr(newobj, field.name)
                values = getattr(self, field.name).all()
                objfield.set(values)

        newobj.save()
        signals.post_duplicate.send(sender=origin, instance=self, duplicate=newobj)
        return newobj

    duplicate.alters_data = True


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
    root_object = InheritanceForeignKey(
        RootObject, blank=True, null=True, on_delete=models.CASCADE
    )

    objects = UriManager()

    def __str__(self):
        return str(self.uri)

    def get_web_object(self):
        result = {
            "relation_pk": self.pk,
            "relation_type": "uri",
            "related_root_object": self.root_object.name,
            "related_root_object_url": self.root_object.get_absolute_url(),
            "related_root_object_class_name": self.root_object.__class__.__name__.lower(),
            "uri": self.uri,
        }
        return result

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self.uri = clean_uri(self.uri)
        if self.uri and not hasattr(self, "root_object"):
            try:
                definition, attributes = rdf.get_definition_and_attributes_from_uri(
                    self.uri
                )
                if definition.getattr("model", False) and attributes:
                    app_label, model = definition.getattr("model").split(".", 1)
                    ct = ContentType.objects.get_by_natural_key(app_label, model)
                    obj = ct.model_class()(**attributes)
                    obj.save()
                    self.root_object = obj
                else:
                    raise ImproperlyConfigured(
                        f"{self.uri}: did not find matching rdf defintion"
                    )
            except Exception as e:
                raise ValidationError(f"{e}: {self.uri}")
