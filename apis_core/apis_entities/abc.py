from pathlib import Path

from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from apis_core.generic.utils.rdf_namespace import CRM
from apis_core.utils.rdf import load_uri_using_path

#########################
# Abstract base classes #
#########################


# These abstract base classes are named after
# CIDOC CRM entities, but we are *NOT*(!)
# trying to implement CIDOC CRM in Django.

RDF_CONFIG_FOLDER = Path(__file__).parent / "triple_configs"


class E21_Person(models.Model):
    forename = models.CharField(
        blank=True, default="", max_length=4096, verbose_name=_("forename")
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
        if self.forename and self.surname:
            return f"{self.forename} {self.surname}"
        return self.forename or self.surname or force_str(_("No name"))

    import_definitions = {
        "https://d-nb.info/*|/.*.rdf": lambda x: load_uri_using_path(
            x, RDF_CONFIG_FOLDER / "E21_PersonFromDNB.toml"
        ),
        "http://www.wikidata.org/*|/.*.rdf": lambda x: load_uri_using_path(
            x, RDF_CONFIG_FOLDER / "E21_PersonFromWikidata.toml"
        ),
    }

    @classmethod
    def get_rdf_types(cls):
        return [CRM.E21_Person]


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
        help_text='<a href="https://www.geonames.org/export/codes.html" target="_blank">Geonames Feature Code List</a>',
    )

    class Meta:
        abstract = True
        verbose_name = _("place")
        verbose_name_plural = _("places")
        ordering = ["label"]

    def __str__(self):
        return self.label or force_str(_("No label"))

    import_definitions = {
        "https://d-nb.info/*|/.*.rdf": lambda x: load_uri_using_path(
            x, RDF_CONFIG_FOLDER / "E53_PlaceFromDNB.toml"
        ),
        "https://sws.geonames.org/*|/.*.rdf*": lambda x: load_uri_using_path(
            x, RDF_CONFIG_FOLDER / "E53_PlaceFromGeonames.toml"
        ),
        "http://www.wikidata.org/*|/.*.rdf": lambda x: load_uri_using_path(
            x, RDF_CONFIG_FOLDER / "E53_PlaceFromWikidata.toml"
        ),
    }

    @classmethod
    def get_rdf_types(cls):
        return [CRM.E53_Place]

    @classmethod
    def create_from_string(cls, string):
        return cls.objects.create(label=string)


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
        return self.label or force_str(_("No label"))

    import_definitions = {
        "https://d-nb.info/*|/.*.rdf": lambda x: load_uri_using_path(
            x, RDF_CONFIG_FOLDER / "E74_GroupFromDNB.toml"
        ),
        "http://www.wikidata.org/*|/.*.rdf": lambda x: load_uri_using_path(
            x, RDF_CONFIG_FOLDER / "E74_GroupFromWikidata.toml"
        ),
    }

    @classmethod
    def get_rdf_types(cls):
        return [CRM.E74_Group]

    @classmethod
    def create_from_string(cls, string):
        return cls.objects.create(label=string)


class SimpleLabelModel(models.Model):
    label = models.CharField(
        blank=True, default="", max_length=4096, verbose_name=_("label")
    )

    class Meta:
        abstract = True
        ordering = ["label"]

    def __str__(self):
        return self.label or force_str(_("No label"))

    @classmethod
    def create_from_string(cls, string):
        return cls.objects.create(label=string)
