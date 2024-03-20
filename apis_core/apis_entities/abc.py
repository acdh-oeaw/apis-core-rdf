from django.db import models

#########################
# Abstract base classes #
#########################


# These abstract base classes are named after
# CIDOC CRM entities, but we are *NOT*(!)
# trying to implement CIDOC CRM in Django.


class E21_Person(models.Model):
    forename = models.CharField(blank=True, default="")
    surname = models.CharField(blank=True, default="")
    gender = models.CharField(blank=True, default="")
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class E53_Place(models.Model):
    label = models.CharField(blank=True, default="")
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True


class E74_Group(models.Model):
    label = models.CharField(blank=True, default="")

    class Meta:
        abstract = True
