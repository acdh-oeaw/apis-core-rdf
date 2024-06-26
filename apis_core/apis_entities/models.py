import re
import functools

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse, NoReverseMatch
from django.db.models.query import QuerySet

from apis_core.apis_metainfo.models import RootObject, Uri
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

    def get_edit_url(self):
        """
        We override the edit url, because entities have a
        custom view that includes the relations
        """
        ct = ContentType.objects.get_for_model(self)
        return reverse(
            "apis_core:apis_entities:generic_entities_edit_view",
            args=[ct.model, self.id],
        )

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

    def get_merge_url(self):
        entity = self.__class__.__name__.lower()
        return reverse(
            "apis_core:apis_entities:generic_entities_merge_view",
            kwargs={"contenttype": entity, "pk": self.id},
        )

    def merge_charfield(self, other, field):
        res = getattr(self, field.name)
        if not field.choices:
            otherres = getattr(other, field.name, res)
            if otherres != res:
                res += f" ({otherres})"
        setattr(self, field.name, res)

    def merge_textfield(self, other, field):
        res = getattr(self, field.name)
        if getattr(other, field.name):
            res += "\n" + f"Merged from {other}:\n" + getattr(other, field.name)
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
        if self in entities:
            entities.remove(self)
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
                self_model_class.objects.get(pk=ent) if isinstance(ent, int) else ent
                for ent in entities
            ]
        for ent in entities:
            e_b = type(ent).__name__
            if e_a != e_b:
                continue
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
def create_default_uri(sender, instance, created, raw, using, update_fields, **kwargs):
    create_default_uri = getattr(settings, "CREATE_DEFAULT_URI", True)
    skip_default_uri = getattr(instance, "skip_default_uri", False)
    if create_default_uri and not skip_default_uri:
        if isinstance(instance, AbstractEntity) and created:
            base = BASE_URI.strip("/")
            try:
                route = reverse("GetEntityGenericRoot", kwargs={"pk": instance.pk})
            except NoReverseMatch:
                route = reverse(
                    "apis_core:GetEntityGeneric", kwargs={"pk": instance.pk}
                )
            uri = f"{base}{route}"
            Uri.objects.create(uri=uri, domain="apis default", root_object=instance)
