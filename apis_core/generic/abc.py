from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


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
