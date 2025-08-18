from django.db import models

from apis_core.generic.abc import GenericModel


class Person(models.Model, GenericModel):
    first_name = models.CharField()
    last_name = models.CharField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Dummy(models.Model, GenericModel):
    pass
