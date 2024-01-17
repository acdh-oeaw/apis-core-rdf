import re

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.query import QuerySet

from apis_core.utils import caching
from apis_core.apis_metainfo.models import RootObject
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
        except Exception as e:
            print("Found no object corresponding to given uri." + e)
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
