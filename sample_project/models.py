from django.db import models
from django.db.models import OuterRef, QuerySet, Subquery

from apis_core.apis_entities.abc import E21_Person, E53_Place, E74_Group
from apis_core.apis_entities.models import AbstractEntity
from apis_core.generic.abc import GenericModel
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation


class Profession(GenericModel, models.Model):
    name = models.CharField(blank=True, default="", max_length=1024)

    def __str__(self):
        return self.name


class Person(VersionMixin, E21_Person, AbstractEntity):
    profession = models.ManyToManyField(Profession, blank=True)


class PlaceQuerySet(QuerySet):
    def with_a_resident(self):
        return self.annotate(
            # Subquery to get the name of a resident
            resident_id=Subquery(
                LivesIn.objects.filter(obj_object_id=OuterRef("id")).values(
                    "subj_object_id"
                )[:1]
            ),
            resident_name=Subquery(
                Person.objects.filter(id=OuterRef("resident_id")).values("forename")[:1]
            ),
        )


class PlaceManager(models.Manager):
    def get_queryset(self):
        return PlaceQuerySet(self.model, using=self._db).with_a_resident()


class Place(VersionMixin, E53_Place, AbstractEntity):
    objects = PlaceManager()


class Group(VersionMixin, E74_Group, AbstractEntity):
    pass


class IsCousinOf(Relation):
    subj_model = Person
    obj_model = Person

    @classmethod
    def reverse_name(self) -> str:
        return "is cousin of"


class IsPartOf(Relation):
    subj_model = Person
    obj_model = Group

    @classmethod
    def reverse_name(self) -> str:
        return "consists of"


class IsSiblingOf(Relation):
    subj_model = Person
    obj_model = Person

    @classmethod
    def reverse_name(self) -> str:
        return "is sibling of"


class LivesIn(Relation):
    subj_model = Person
    obj_model = Place

    @classmethod
    def reverse_name(self) -> str:
        return "has inhabitant"
