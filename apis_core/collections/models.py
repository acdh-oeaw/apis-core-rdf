from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apis_core.generic.abc import GenericModel


class SkosCollectionManager(models.Manager):
    def get_by_full_path(self, name: str):
        """
        Return a collection specified by its full path, from the root colletion
        to the leaf collection, delimited by `|`. I.e. if there is a collection
        named `foo` and it has a parent named `bar` and `bar` does not have a
        parent, then you can use the string "bar|foo" to get the `foo` collection.
        """
        names = name.split("|")
        parent = None
        while names:
            parent = self.get(parent=parent, name=names.pop(0))
        return parent


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
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "name",
                    "parent",
                ),
                name="unique_name_parent",
                nulls_distinct=False,
                violation_error_message="The combination of name and parent collection must be unique",
            ),
            models.CheckConstraint(
                check=~models.Q(name__contains="|"),
                name="check_name_pipe",
                violation_error_message="The name must not contain the pipe symbol: |",
            ),
        ]

    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE, blank=True)
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

    def children(self):
        return SkosCollection.objects.filter(parent=self)

    def children_tree_as_list(self):
        childtrees = [self]
        for child in self.children():
            childtrees.extend(child.children_tree_as_list())
        return childtrees


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
