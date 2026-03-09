from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class SearchManager(models.Manager):
    def search(self, q, content_types=[]):
        query = super().get_queryset().filter(title__icontains=q)
        if content_types:
            query = super().get_queryset().filter(content_types__in=content_types)
        return query


class SearchEntry(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    title = models.CharField(max_length=1024)
    description = models.TextField()

    content = models.JSONField()

    objects = SearchManager()

    class Meta:
        unique_together = ["content_type", "object_id"]
        # indexes = [GinIndex(fields=["content"])]
