from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from apis_core.generic.helpers import permission_fullname


class GenericModel:
    @classmethod
    def get_listview_url(cls):
        ct = ContentType.objects.get_for_model(cls)
        return reverse("apis_core:generic:list", args=[ct])

    @classmethod
    def get_createview_url(cls):
        ct = ContentType.objects.get_for_model(cls)
        return reverse("apis_core:generic:create", args=[ct])

    def get_edit_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:update", args=[ct, self.id])

    def get_absolute_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:detail", args=[ct, self.id])

    def get_delete_url(self):
        ct = ContentType.objects.get_for_model(self)
        return reverse("apis_core:generic:delete", args=[ct, self.id])

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
