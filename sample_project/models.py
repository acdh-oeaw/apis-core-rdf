from django.db import models

from apis_core.apis_entities.abc import E21_Person, E53_Place, E74_Group
from apis_core.apis_entities.models import AbstractEntity
from apis_core.generic.abc import GenericModel
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation


class Profession(VersionMixin, GenericModel, models.Model):
    name = models.CharField(blank=True, default="", max_length=1024)

    def __str__(self):
        return self.name


class Person(VersionMixin, E21_Person, AbstractEntity):
    profession = models.ManyToManyField(Profession, blank=True)


class Place(VersionMixin, E53_Place, AbstractEntity):
    pass


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
