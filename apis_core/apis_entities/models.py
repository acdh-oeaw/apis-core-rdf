import re
import re
import unicodedata
import json

from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.urls import reverse
from model_utils.managers import InheritanceManager
from django.db.models.query import QuerySet

from apis_core.utils import caching
from apis_core.utils import DateParser
from apis_core.apis_metainfo.models import RootObject, Collection
from apis_core.apis_relations.models import TempTriple
from apis_core.apis_entities import signals

BASE_URI = getattr(settings, "APIS_BASE_URI", "http://apis.info/")
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        if self.name != "":
            return self.name
        else:
            return "no name provided"

    @classmethod
    def get_or_create_uri(cls, uri):
        uri = str(uri)
        try:
            if re.match(r"^[0-9]*$", uri):
                p = cls.objects.get(pk=uri)
            else:
                p = cls.objects.get(uri__uri=uri)
            return p
        except:
            print("Found no object corresponding to given uri.")
            return False

    # TODO
    @classmethod
    def get_entity_list_filter(cls):
        return None

    @classmethod
    def get_listview_url(self):
        entity = self.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_list",
            kwargs={"entity": entity},
        )

    @classmethod
    def get_createview_url(self):
        entity = self.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_create_view",
            kwargs={"entity": entity},
        )

    def get_edit_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_edit_view",
            kwargs={"entity": entity, "pk": self.id},
        )

    def get_absolute_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_detail_view",
            kwargs={"entity": entity, "pk": self.id},
        )

    def get_prev_url(self):
        entity = self.__class__.__name__.lower()
        if NEXT_PREV:
            prev = self.__class__.objects.filter(id__lt=self.id).order_by("-id")
        else:
            return False
        if prev:
            return reverse(
                "apis_core:apis_entities:generic_entities_detail_view",
                kwargs={"entity": entity, "pk": prev.first().id},
            )
        else:
            return False

    def get_next_url(self):
        entity = self.__class__.__name__.lower()
        if NEXT_PREV:
            next = self.__class__.objects.filter(id__gt=self.id)
        else:
            return False
        if next:
            return reverse(
                "apis_core:apis_entities:generic_entities_detail_view",
                kwargs={"entity": entity, "pk": next.first().id},
            )
        else:
            return False

    def get_delete_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_delete_view",
            kwargs={"entity": entity, "pk": self.id},
        )

    def get_duplicate_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_duplicate_view",
            kwargs={"entity": entity, "pk": self.id},
        )

    def merge_charfield(self, other, field):
        print(field)
        res = getattr(self, field.name)
        if not field.choices:
            if getattr(other, field.name):
                res += " (" + getattr(other, field.name) + ")"
        setattr(self, field.name, res)

    def merge_textfield(self, other, field):
        res = getattr(self, field.name)
        if getattr(other, field.name):
            res += "\n" + "Merged from {other}\n" + getattr(other, field.name)
        setattr(self, field.name, res)

    def merge_booleanfield(self, other, field):
        setattr(
            self, field.name, getattr(self, field.name) and getattr(other, field.name)
        )

    def merge_start_date_written(self, other):
        self.start_date_written = self.start_date_written or other.start_date_written

    def merge_end_date_written(self, other):
        self.end_date_written = self.end_date_written or other.end_date_written

    def merge_fields(self, other):
        """
        This method iterates through the model fields and copies
        data from other to self. It first tries to find a merge method
        that is specific to that field (merge_{fieldname}) and then tries
        to find a method that is specific to the type of the field (merge_{fieldtype})
        It is called by the `merge_with` method.
        """
        for field in self._meta.fields:
            fieldtype = field.get_internal_type().lower()
            # if there is a `merge_{fieldname}` method in this model, use that one
            if callable(getattr(self, f"merge_{field.name}", None)):
                getattr(self, f"merge_{field.name}")(other)
            # otherwise we check if there is a method for the field type and use that one
            elif callable(getattr(self, f"merge_{fieldtype}", None)):
                getattr(self, f"merge_{fieldtype}")(other, field)
            else:
                if not getattr(self, field.name):
                    setattr(self, field.name, getattr(other, field.name))
        self.save()

    def merge_with(self, entities):
        origin = self.__class__
        signals.pre_merge_with.send(sender=origin, instance=self, entities=entities)

        # TODO: check if these imports can be put to top of module without
        #  causing circular import issues.
        from apis_core.apis_metainfo.models import Uri

        e_a = type(self).__name__
        self_model_class = ContentType.objects.get(model__iexact=e_a).model_class()
        if isinstance(entities, int):
            entities = self_model_class.objects.get(pk=entities)
        if not isinstance(entities, list) and not isinstance(entities, QuerySet):
            entities = [entities]
            entities = [
                self_model_class.objects.get(pk=ent) if type(ent) == int else ent
                for ent in entities
            ]
        for ent in entities:
            e_b = type(ent).__name__
            if e_a != e_b:
                continue
            # TODO: if collections are removed, remove this as well
            if hasattr(ent, "collection"):
                col_list = list(self.collection.all())
                for col2 in ent.collection.all():
                    if col2 not in col_list:
                        self.collection.add(col2)
            for f in ent._meta.local_many_to_many:
                if not f.name.endswith("_set"):
                    sl = list(getattr(self, f.name).all())
                    for s in getattr(ent, f.name).all():
                        if s not in sl:
                            getattr(self, f.name).add(s)
            Uri.objects.filter(root_object=ent).update(root_object=self)
            TempTriple.objects.filter(obj__id=ent.id).update(obj=self)
            TempTriple.objects.filter(subj__id=ent.id).update(subj=self)

        for ent in entities:
            self.merge_fields(ent)

        signals.post_merge_with.send(sender=origin, instance=self, entities=entities)

        for ent in entities:
            ent.delete()

    def get_serialization(self):
        from apis_core.apis_entities.serializers_generic import EntitySerializer

        return EntitySerializer(self).data


class TempEntityClass(AbstractEntity):
    """
    Base class to bind common attributes to many classes.

    The common attributes are:
    - written start and enddates,
    - recognized start and enddates which are derived from the written dates
    using RegEx,
    - a review boolean field to mark an object as reviewed.
    """

    review = models.BooleanField(
        default=False,
        help_text="Should be set to True, if the "
        "data record holds up quality "
        "standards.",
    )
    start_date = models.DateField(blank=True, null=True)
    start_start_date = models.DateField(blank=True, null=True)
    start_end_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_start_date = models.DateField(blank=True, null=True)
    end_end_date = models.DateField(blank=True, null=True)
    start_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Start",
    )
    end_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="End",
    )
    # TODO RDF: Make Text also a Subclass of RootObject
    collection = models.ManyToManyField("apis_metainfo.Collection")
    status = models.CharField(max_length=100)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    objects = models.Manager()
    objects_inheritance = InheritanceManager()

    def __str__(self):
        if self.name != "" and hasattr(
            self, "first_name"  # TODO RDF: remove first_name here
        ):  # relation usually don´t have names
            return "{}, {} (ID: {})".format(self.name, self.first_name, self.id)
        elif self.name != "":
            return "{} (ID: {})".format(self.name, self.id)
        else:
            return "(ID: {})".format(self.id)

    def save(self, parse_dates=True, *args, **kwargs):
        """
        Adaption of the save() method of the class to automatically parse
        string-dates into date objects.
        """

        if parse_dates:
            # overwrite every field with None as default
            start_date = None
            start_start_date = None
            start_end_date = None
            end_date = None
            end_start_date = None
            end_end_date = None

            # if some textual user input of a start date is there, parse it
            if self.start_date_written:
                start_date, start_start_date, start_end_date = DateParser.parse_date(
                    self.start_date_written
                )

            # if some textual user input of an end date is there, parse it
            if self.end_date_written:
                end_date, end_start_date, end_end_date = DateParser.parse_date(
                    self.end_date_written
                )

            self.start_date = start_date
            self.start_start_date = start_start_date
            self.start_end_date = start_end_date
            self.end_date = end_date
            self.end_start_date = end_start_date
            self.end_end_date = end_end_date

        if self.name:
            self.name = unicodedata.normalize("NFC", self.name)

        super(TempEntityClass, self).save(*args, **kwargs)

        return self


def prepare_fields_dict(fields_list, vocabs, vocabs_m2m):
    res = dict()
    for f in fields_list:
        res[f["name"]] = getattr(models, f["field_type"])(**f["attributes"])
    for v in vocabs:
        res[v] = models.ForeignKey(
            f"apis_vocabularies.{v}", blank=True, null=True, on_delete=models.SET_NULL
        )
    for v2 in vocabs_m2m:
        res[v2] = models.ManyToManyField(f"apis_vocabularies.{v2}", blank=True)
    return res


@receiver(post_save, dispatch_uid="create_default_uri")
def create_default_uri(sender, instance, raw, **kwargs):
    # with django reversion, browsing deleted entries in the admin interface
    # leads to firing the `post_save` signal
    # (https://github.com/etianen/django-reversion/issues/936) - a workaround
    # is to check for the raw argument
    if not raw:
        from apis_core.apis_metainfo.models import Uri

        if kwargs["created"] and sender in caching.get_all_ontology_classes():
            if BASE_URI.endswith("/"):
                base1 = BASE_URI[:-1]
            else:
                base1 = BASE_URI
            uri_c = "{}{}".format(
                base1,
                reverse("GetEntityGenericRoot", kwargs={"pk": instance.pk}),
            )
            uri2 = Uri(uri=uri_c, domain="apis default", root_object=instance)
            uri2.save()


if "registration" in getattr(settings, "INSTALLED_APPS", []):
    from registration.backends.simple.views import RegistrationView
    from registration.signals import user_registered

    @receiver(
        user_registered,
        sender=RegistrationView,
        dispatch_uid="add_registered_user_to_group",
    )
    def add_user_to_group(sender, user, request, **kwargs):
        user_group = getattr(settings, "APIS_AUTO_USERGROUP", None)
        if user_group is not None:
            user.groups.add(Group.objects.get(name=user_group))
