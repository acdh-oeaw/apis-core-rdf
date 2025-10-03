from django.db import models

from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation


class Profession(VersionMixin, models.Model):
    label = models.CharField()


class Person(VersionMixin, models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    profession = models.ManyToManyField(Profession, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Place(VersionMixin, models.Model):
    label = models.CharField()


class PersonPlaceRelation(VersionMixin, Relation):
    subj_model = Person
    obj_model = Place
