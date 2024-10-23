from django.contrib.contenttypes.models import ContentType
from django.db.models import BooleanField, CharField, TextField
from django.urls import reverse

from apis_core.generic.helpers import permission_fullname


class GenericModel:
    def __repr__(self):
        return super().__repr__() + f" (ID: {self.id})"

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

    def get_edit_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:update", args=[ct, self.id])

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
