from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.indexes import GinIndex
from django.db import models


class SearchEntry(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    title = models.CharField(max_length=1024)
    description = models.TextField()

    content = models.JSONField()

    class Meta:
        unique_together = ["content_type", "object_id"]
        indexes = [GinIndex(fields=["content"])]
