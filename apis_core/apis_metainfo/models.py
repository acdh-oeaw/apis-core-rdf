from django.db import models
from model_utils.managers import InheritanceManager

from apis_core.generic.abc import GenericModel


class RootObject(GenericModel, models.Model):
    """
    The very root thing that can exist in a given ontology. Several classes inherit from it.
    By having one overarching super class we gain the advantage of unique identifiers.
    """

    objects = models.Manager()
    objects_inheritance = InheritanceManager()
