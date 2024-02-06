from django.db import models
from apis_core.apis_entities.models import AbstractEntity


class Character(AbstractEntity):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)


class Place(AbstractEntity):
    name2 = models.CharField(max_length=255, blank=True)


class Book(AbstractEntity):
    title = models.CharField(max_length=255, blank=True)
