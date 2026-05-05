from django.urls import reverse

from apis_core.generic.abc import GenericModel


class Entity(GenericModel):
    class Meta:
        abstract = True

    @property
    def get_canonical_url(self):
        return reverse("apis_core:canonical-entity", args=[self.pk])
