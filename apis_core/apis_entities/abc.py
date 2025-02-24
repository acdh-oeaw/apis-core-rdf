from pathlib import Path

from django.db import models

#########################
# Abstract base classes #
#########################


# These abstract base classes are named after
# CIDOC CRM entities, but we are *NOT*(!)
# trying to implement CIDOC CRM in Django.


class E21_Person(models.Model):
    forename = models.CharField(blank=True, default="", max_length=4096)
    surname = models.CharField(blank=True, default="", max_length=4096)
    gender = models.CharField(blank=True, default="", max_length=4096)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.forename} {self.surname}"

    @classmethod
    def rdf_configs(cls):
        return [
            Path(__file__).parent / "triple_configs/E21_PersonFromDNB.toml",
            Path(__file__).parent / "triple_configs/E21_PersonFromWikidata.toml",
        ]


class E53_Place(models.Model):
    label = models.CharField(blank=True, default="", max_length=4096)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label

    @classmethod
    def rdf_configs(cls):
        return [
            Path(__file__).parent / "triple_configs/E53_PlaceFromDNB.toml",
            Path(__file__).parent / "triple_configs/E53_PlaceFromGeonames.toml",
            Path(__file__).parent / "triple_configs/E53_PlaceFromWikidata.toml",
        ]


class E74_Group(models.Model):
    label = models.CharField(blank=True, default="", max_length=4096)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label

    @classmethod
    def rdf_configs(cls):
        return [
            Path(__file__).parent / "triple_configs/E74_GroupFromDNB.toml",
            Path(__file__).parent / "triple_configs/E74_GroupFromWikidata.toml",
        ]
