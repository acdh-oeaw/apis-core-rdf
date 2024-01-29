from django.db import models


class LabelBaseModel(models.Model):
    label = models.CharField(blank=True, default="")

    class Meta:
        abstract = True
