from django.db import models

from apis_core.apis_entities.abc import E21_Person, E53_Place, E74_Group
from apis_core.apis_entities.models import AbstractEntity
from apis_core.generic.abc import GenericModel
from apis_core.history.models import VersionMixin


class Profession(GenericModel, models.Model):
    name = models.CharField(blank=True, default="", max_length=1024)


class Person(VersionMixin, E21_Person, AbstractEntity):
    profession = models.ManyToManyField(Profession, blank=True)


class Place(VersionMixin, E53_Place, AbstractEntity):
    pass


class Group(VersionMixin, E74_Group, AbstractEntity):
    pass
