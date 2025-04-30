from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apis_core.generic.abc import GenericModel


class SkosCollectionManager(models.Manager):
    def by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance)
        scco = SkosCollectionContentObject.objects.filter(
            content_type=content_type, object_id=instance.id
        )
        return self.get_queryset().filter(
            pk__in=scco.values_list("collection", flat=True)
        )


class SkosCollection(GenericModel, models.Model):
    """
    SKOS collections are labeled and/or ordered groups of SKOS concepts.
    Collections are useful where a group of concepts shares something in common,
    and it is convenient to group them under a common label, or
    where some concepts can be placed in a meaningful order.

    Miles, Alistair, and Sean Bechhofer. "SKOS simple knowledge
    organization system reference. W3C recommendation (2009)."

    """

    class Meta:
        ordering = ["name"]

    name = models.CharField(
        max_length=300,
        verbose_name="skos:prefLabel",
        help_text="Collection label or name",
    )
    label_lang = models.CharField(
        max_length=3,
        blank=True,
        default="en",
        verbose_name="skos:prefLabel language",
        help_text="Language of preferred label given above",
    )
    creator = models.TextField(
        blank=True,
        verbose_name="dc:creator",
        help_text="Person or organisation that created this collection"
        "If more than one list all using a semicolon ;",
    )
    contributor = models.TextField(
        blank=True,
        verbose_name="dc:contributor",
        help_text="Person or organisation that made contributions to the collection"
        "If more than one list all using a semicolon ;",
    )
    objects = SkosCollectionManager()

    def __str__(self):
        return self.name

    def add(self, instance: object):
        content_type = ContentType.objects.get_for_model(instance)
        SkosCollectionContentObject.objects.get_or_create(
            collection=self, content_type=content_type, object_id=instance.pk
        )

    def remove(self, instance: object):
        content_type = ContentType.objects.get_for_model(instance)
        SkosCollectionContentObject.objects.filter(
            collection=self, content_type=content_type, object_id=instance.pk
        ).delete()

    @property
    def parent_collection(self):
        content_type = ContentType.objects.get_for_model(self)
        sccos = SkosCollectionContentObject.objects.filter(
            content_type=content_type, object_id=self.id
        )
        if len(sccos) == 1:
            return sccos.first().collection
        raise SkosCollection.MultipleObjectsReturned(
            f'"{self}" is part of multiple collections'
        )


class SkosCollectionContentObject(GenericModel, models.Model):
    """
    *Throughtable* datamodel to connect collections to arbitrary content
    """

    collection = models.ForeignKey(SkosCollection, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.content_object} -> {self.collection}"
