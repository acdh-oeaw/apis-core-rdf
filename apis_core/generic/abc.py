import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models import BooleanField, CharField, TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.query import QuerySet
from django.forms import model_to_dict
from django.urls import reverse

from apis_core.generic.helpers import mro_paths, permission_fullname
from apis_core.generic.signals import (
    post_duplicate,
    post_merge_with,
    pre_duplicate,
    pre_merge_with,
)
from apis_core.utils.settings import apis_base_uri, rdf_namespace_prefix

logger = logging.getLogger(__name__)


class GenericModel:
    def __repr__(self):
        if id := getattr(self, "id", None):
            return super().__repr__() + f" (ID: {id})"
        return super().__repr__()

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @classmethod
    def get_listview_url(cls):
        ct = ContentType.objects.get_for_model(cls)
        return reverse("apis_core:generic:list", args=[ct])

    @classmethod
    def get_createview_url(cls):
        ct = ContentType.objects.get_for_model(cls)
        return reverse("apis_core:generic:create", args=[ct])

    @classmethod
    def get_importview_url(cls):
        ct = ContentType.objects.get_for_model(cls)
        return reverse("apis_core:generic:import", args=[ct])

    @classmethod
    def get_openapi_tags(cls):
        return [item[-1] for item in mro_paths(cls)]

    @classmethod
    def get_namespace_prefix(cls):
        ct = ContentType.objects.get_for_model(cls)
        return f"{rdf_namespace_prefix()}-{ct.model}"

    @classmethod
    def get_namespace_uri(cls):
        return apis_base_uri() + cls.get_listview_url()

    @classmethod
    def get_rdf_types(cls):
        return []

    def get_edit_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:update", args=[ct, self.id])

    def get_duplicate_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:duplicate", args=[ct, self.id])

    def get_enrich_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:enrich", args=[ct, self.id])

    def get_absolute_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:detail", args=[ct, self.id])

    def get_delete_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:delete", args=[ct, self.id])

    def get_merge_url(self, other_id):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:merge", args=[ct, self.id, other_id])

    def get_select_merge_or_enrich_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:selectmergeorenrich", args=[ct, self.id])

    def get_create_success_url(self):
        return self.get_absolute_url()

    def get_update_success_url(self):
        return self.get_edit_url()

    def get_api_detail_endpoint(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:genericmodelapi-detail", args=[ct, self.id])

    @classmethod
    def get_change_permission(self):
        return permission_fullname("change", self)

    @classmethod
    def get_add_permission(self):
        return permission_fullname("add", self)

    @classmethod
    def get_delete_permission(self):
        return permission_fullname("delete", self)

    @classmethod
    def get_view_permission(self):
        return permission_fullname("view", self)

    @classmethod
    def get_verbose_name_plural(cls):
        return cls._meta.verbose_name_plural

    def get_merge_charfield_value(self, other: CharField, field: CharField):
        res = getattr(self, field.name)
        if not field.choices:
            otherres = getattr(other, field.name, res)
            if otherres != res:
                res += f" ({otherres})"
        return res

    def get_merge_textfield_value(self, other: TextField, field: TextField):
        res = getattr(self, field.name)
        if getattr(other, field.name):
            res += "\n" + f"Merged from {other}:\n" + getattr(other, field.name)
        return res

    def get_merge_booleanfield(self, other: BooleanField, field: BooleanField):
        return getattr(other, field.name)

    def get_field_value_after_merge(self, other, field):
        """
        This method finds the value of a field after merging `other` into `self`.
        It first tries to find a merge method that is specific to that field
        (merge_{fieldname}) and then tries to find a method that is specific to
        the type of the field (merge_{fieldtype})
        If neither of those exist, it uses the others field value if the field
        in self is not set, otherwise it keeps the value in self.
        """
        fieldtype = field.get_internal_type().lower()
        # if there is a `get_merge_{fieldname}` method in this model, use that one
        if callable(getattr(self, f"get_merge_{field.name}_value", None)):
            return getattr(self, f"get_merge_{field.name}_value")(other)
        # otherwise we check if there is a method for the field type and use that one
        elif callable(getattr(self, f"get_merge_{fieldtype}_value", None)):
            return getattr(self, f"get_merge_{fieldtype}_value")(other, field)
        else:
            if not getattr(self, field.name):
                return getattr(other, field.name)
        return getattr(self, field.name)

    def merge_fields(self, other):
        """
        This method iterates through the model fields and uses the
        `get_field_value_after_merge` method to copy values from `other` to `self`.
        It is called by the `merge_with` method.
        """
        for field in self._meta.fields:
            newval = self.get_field_value_after_merge(other, field)
            if newval != getattr(self, field.name):
                setattr(self, field.name, newval)
        self.save()

    def merge_with(self, entities):
        if self in entities:
            entities.remove(self)
        origin = self.__class__
        pre_merge_with.send(sender=origin, instance=self, entities=entities)

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
            self_content_type = ContentType.objects.get_for_model(self)
            ent_content_type = ContentType.objects.get_for_model(ent)
            Uri.objects.filter(content_type=ent_content_type, object_id=ent.id).update(
                content_type=self_content_type, object_id=self.id
            )

        for ent in entities:
            self.merge_fields(ent)

        post_merge_with.send(sender=origin, instance=self, entities=entities)

        for ent in entities:
            ent.delete()

    def duplicate(self):
        origin = self.__class__
        pre_duplicate.send(sender=origin, instance=self)
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
        post_duplicate.send(sender=origin, instance=self, duplicate=newobj)
        return newobj

    duplicate.alters_data = True

    def uri_set(self):
        ct = ContentType.objects.get_for_model(self)
        return (
            ContentType.objects.get(app_label="apis_metainfo", model="uri")
            .model_class()
            .objects.filter(content_type=ct, object_id=self.id)
            .all()
        )
