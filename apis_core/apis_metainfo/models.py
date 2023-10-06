import re
from difflib import SequenceMatcher
from math import inf
import copy
import importlib

import requests

# from reversion import revisions as reversion
import reversion
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.fields.related import OneToOneField, ForeignKey, ManyToManyField
from django.forms import model_to_dict
from django.urls import reverse
from django.utils.functional import cached_property
from model_utils.managers import InheritanceManager
from apis_core.utils.normalize import clean_uri
from django.core.exceptions import ValidationError, ImproperlyConfigured

# from django.contrib.contenttypes.fields import GenericRelation
# from utils.highlighter import highlight_text
from apis_core.utils import caching, rdf

from apis_core.apis_metainfo import signals

# from apis_core.apis_entities.serializers_generic import EntitySerializer
# from apis_core.apis_labels.models import Label
# from apis_core.apis_vocabularies.models import CollectionType, LabelType, TextType

path_ac_settings = getattr(settings, "APIS_AUTOCOMPLETE_SETTINGS", False)
if path_ac_settings:
    ac_settings = importlib.import_module(path_ac_settings)
    autocomp_settings = getattr(ac_settings, "autocomp_settings")
else:
    from apis_core.default_settings.NER_settings import autocomp_settings
# from apis_core.utils import DateParser

NEXT_PREV = getattr(settings, "APIS_NEXT_PREV", True)


@reversion.register()
class RootObject(models.Model):
    """
    The very root thing that can exist in a given ontology. Several classes inherit from it.
    By having one overarching super class we gain the advantage of unique identifiers.
    """

    name = models.CharField(max_length=255, verbose_name="Name")
    # self_contenttype: a foreign key to the respective contenttype comes in handy when querying for
    # triples where the subject's or object's contenttype must be respected (e.g. get all triples
    # where the subject is a Person)
    self_contenttype = models.ForeignKey(
        ContentType, on_delete=models.deletion.CASCADE, null=True, blank=True
    )
    objects = models.Manager()
    objects_inheritance = InheritanceManager()

    def save(self, *args, **kwargs):
        if self.self_contenttype is None:
            self.self_contenttype = caching.get_contenttype_of_class(self.__class__)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.name != "":
            return self.name
        else:
            return "no name provided"

    def duplicate(self):
        origin = self.__class__
        signals.pre_duplicate.send(sender=origin, instance=self)
        # usually, copying instances would work like
        # https://docs.djangoproject.com/en/4.2/topics/db/queries/#copying-model-instances
        # but we are working with abstract classes,
        # so we have to do it by hand  using model_to_dict:(
        objdict = model_to_dict(self)
        objdict.pop("id")

        # remove related fields from dict representation
        related_fields = [
            field for field in self._meta.get_fields() if field.is_relation
        ]
        for field in related_fields:
            objdict.pop(field.name, None)

        entity_model = caching.get_entity_class_of_name(self._meta.model_name)
        newobj = entity_model.objects.create(**objdict)

        for field in related_fields:
            # we are not using `isinstance` because we want to
            # differentiate between different levels of inheritance
            if type(field) is ForeignKey:
                setattr(newobj, field.name, getattr(self, field.name))
            if type(field) is ManyToManyField:
                objfield = getattr(newobj, field.name)
                values = getattr(self, field.name).all()
                objfield.set(values)

        duplicate = newobj.save()
        signals.post_duplicate.send(sender=origin, instance=self, duplicate=duplicate)
        return duplicate


@reversion.register()
class Collection(models.Model):
    """Allows to group entities and relation."""

    from apis_core.apis_vocabularies.models import CollectionType

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    collection_type = models.ForeignKey(
        CollectionType, blank=True, null=True, on_delete=models.SET_NULL
    )
    groups_allowed = models.ManyToManyField(Group)
    parent_class = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE
    )
    published = models.BooleanField(default=False)

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if hasattr(self, "_loaded_values"):
            if self.published != self._loaded_values["published"]:
                for ent in self.tempentityclass_set.all():
                    ent.published = self.published
                    ent.save()
        super().save(*args, **kwargs)


# TODO: Move this somewhere else so that it can be imported at several places (right now it's redundant with copies)
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


class InheritanceForwardManyToOneDescriptor(ForwardManyToOneDescriptor):
    def get_queryset(self, **hints):
        return self.field.remote_field.model.objects_inheritance.db_manager(
            hints=hints
        ).select_subclasses()


class InheritanceForeignKey(models.ForeignKey):
    forward_related_accessor_class = InheritanceForwardManyToOneDescriptor


# Uri model
# We use a custom UriManager, so we can override the queryset `get_or_create`
# method. This is useful because we normalize the uri field before saving.


class UriQuerySet(models.query.QuerySet):
    def get_or_create(self, defaults=None, **kwargs):
        if "uri" in kwargs:
            kwargs["uri"] = clean_uri(kwargs["uri"])
        return super().get_or_create(defaults, **kwargs)


class UriManager(models.Manager):
    def get_queryset(self):
        return UriQuerySet(self.model)


@reversion.register()
class Uri(models.Model):
    uri = models.URLField(blank=True, null=True, unique=True, max_length=255)
    domain = models.CharField(max_length=255, blank=True)
    rdf_link = models.URLField(blank=True)
    root_object = InheritanceForeignKey(
        RootObject, blank=True, null=True, on_delete=models.CASCADE
    )
    # loaded set to True when RDF was loaded and parsed into the data model
    loaded = models.BooleanField(default=False)
    # Timestamp when file was loaded and parsed
    loaded_time = models.DateTimeField(blank=True, null=True)

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

    @classmethod
    def get_listview_url(self):
        return reverse("apis_core:apis_metainfo:uri_browse")

    @classmethod
    def get_createview_url(self):
        return reverse("apis_core:apis_metainfo:uri_create")

    def get_absolute_url(self):
        return reverse("apis_core:apis_metainfo:uri_detail", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("apis_core:apis_metainfo:uri_delete", kwargs={"pk": self.id})

    def get_edit_url(self):
        return reverse("apis_core:apis_metainfo:uri_edit", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        self.uri = clean_uri(self.uri)
        if self.uri and not hasattr(self, "root_object"):
            try:
                model, attributes = rdf.get_modelname_and_dict_from_uri(self.uri)
                if model and attributes:
                    app_label, model = model.split(".", 1)
                    ct = ContentType.objects.get_by_natural_key(app_label, model)
                    obj = ct.model_class()(**attributes)
                    obj.save()
                    self.root_object = obj
                else:
                    raise ImproperlyConfigured(
                        f"{uri}: found model <{model}> and attributes <{attributes}>"
                    )
            except Exception as e:
                raise ValidationError(f"{e}: {self.uri}")


# @receiver(post_save, sender=Uri, dispatch_uid="remove_default_uri")
# def remove_default_uri(sender, instance, **kwargs):
#    if Uri.objects.filter(root_object=instance.entity).count() > 1:
#        Uri.objects.filter(root_object=instance.entity, domain="apis default").delete()
