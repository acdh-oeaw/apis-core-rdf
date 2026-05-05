import functools

from django.urls import reverse

from apis_core.generic.abc import GenericModel


class Entity(GenericModel):
    class Meta:
        abstract = True

    @property
    def get_canonical_url(self):
        return reverse("apis_core:canonical-entity", args=[self.pk])

    @functools.cached_property
    def get_prev_id(self):
        prev_instance = (
            type(self).objects.filter(id__lt=self.id).order_by("-id").only("id").first()
        )
        if prev_instance is not None:
            return prev_instance.id
        return False

    @functools.cached_property
    def get_next_id(self):
        next_instance = (
            type(self).objects.filter(id__gt=self.id).order_by("id").only("id").first()
        )
        if next_instance is not None:
            return next_instance.id
        return False

    def import_data(self, data):
        super().import_data(data)
        if "same_as" in data:
            self._uris = data["same_as"]
            self.save()
        if "relations" in data:
            self.create_relations_to_uris = data["relations"]
            self.save()
