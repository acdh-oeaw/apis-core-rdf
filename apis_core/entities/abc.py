from django.db import models
from django.urls import reverse


class Entity(models.Model):
    class Meta:
        abstract = True

    @property
    def get_canonical_url(self):
        return reverse("apis_core:canonical-entity", args=[self.id])
