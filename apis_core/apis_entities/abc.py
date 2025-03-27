from pathlib import Path

from django.db import models
from django.utils.translation import gettext_lazy as _

#########################
# Abstract base classes #
#########################


# These abstract base classes are named after
# CIDOC CRM entities, but we are *NOT*(!)
# trying to implement CIDOC CRM in Django.


class E21_Person(models.Model):
    forename = models.CharField(
        blank=True, default="", max_length=4096, verbose_name=_("forname")
    )
    surname = models.CharField(
        blank=True, default="", max_length=4096, verbose_name=_("surname")
    )
    gender = models.CharField(
        blank=True, default="", max_length=4096, verbose_name=_("gender")
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name=_("date of birth")
    )
    date_of_death = models.DateField(
        blank=True, null=True, verbose_name=_("date of death")
    )

    class Meta:
        abstract = True
        verbose_name = _("person")
        verbose_name_plural = _("persons")
        ordering = ["surname", "forename"]

    def __str__(self):
        return f"{self.forename} {self.surname}"

    @classmethod
    def rdf_configs(cls):
        return [
            Path(__file__).parent / "triple_configs/E21_PersonFromDNB.toml",
            Path(__file__).parent / "triple_configs/E21_PersonFromWikidata.toml",
        ]


class E53_Place(models.Model):
    """
    The feature_code field refers to the geonames feature codes, as
    listed on https://www.geonames.org/export/codes.html
    """

    label = models.CharField(
        blank=True, default="", max_length=4096, verbose_name=_("label")
    )
    latitude = models.FloatField(blank=True, null=True, verbose_name=_("latitude"))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_("longitude"))
    feature_code = models.CharField(
        blank=True,
        default="",
        max_length=16,
        verbose_name=_("feature code"),
        help_text='<a href="https://www.geonames.org/export/codes.html">Geonames Feature Code List</a>',
    )

    class Meta:
        abstract = True
        verbose_name = _("place")
        verbose_name_plural = _("places")
        ordering = ["label"]

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
    label = models.CharField(
        blank=True, default="", max_length=4096, verbose_name=_("label")
    )

    class Meta:
        abstract = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        ordering = ["label"]

    def __str__(self):
        return self.label

    @classmethod
    def rdf_configs(cls):
        return [
            Path(__file__).parent / "triple_configs/E74_GroupFromDNB.toml",
            Path(__file__).parent / "triple_configs/E74_GroupFromWikidata.toml",
        ]


class SimpleLabelModel(models.Model):
    label = models.CharField(
        blank=True, default="", max_length=4096, verbose_name=_("label")
    )

    class Meta:
        abstract = True
        ordering = ["label"]

    def __str__(self):
        return self.label

    @classmethod
    def create_from_string(cls, string):
        return cls.objects.create(label=string)
