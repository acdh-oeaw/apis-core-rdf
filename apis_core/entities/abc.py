import functools

from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from apis_core.entities.rdfconfigs import group, person, place
from apis_core.generic.abc import GenericModel, SimpleLabelModel
from apis_core.generic.utils.rdf_namespace import CRM
from apis_core.utils.rdf import load_uri_using_path


class Entity(GenericModel):
    class Meta:
        abstract = True

    @property
    def get_canonical_url(self):
        return reverse("apis_core:canonical-entity", args=[self.pk])

    @functools.cached_property
    def get_prev_id(self):
        prev_instance = (
            type(self).objects.filter(id__lt=self.id).order_by("-id").only("id").first()
        )
        if prev_instance is not None:
            return prev_instance.id
        return False

    @functools.cached_property
    def get_next_id(self):
        next_instance = (
            type(self).objects.filter(id__gt=self.id).order_by("id").only("id").first()
        )
        if next_instance is not None:
            return next_instance.id
        return False

    def import_data(self, data):
        super().import_data(data)
        if "same_as" in data:
            self._uris = data["same_as"]
            self.save()
        if "relations" in data:
            self.create_relations_to_uris = data["relations"]
            self.save()


#########################
# Abstract base classes #
#########################


# These abstract base classes are named after
# CIDOC CRM entities, but we are *NOT*(!)
# trying to implement CIDOC CRM in Django.


class E21_Person(Entity):
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
            x, person.E21_PersonFromDNB
        ),
        "http://www.wikidata.org/*|/.*.rdf": lambda x: load_uri_using_path(
            x, person.E21_PersonFromWikidata
        ),
    }

    @classmethod
    def get_rdf_types(cls):
        return [CRM.E21_Person]


class E53_Place(Entity):
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
            x, place.E53_PlaceFromDNB
        ),
        "https://sws.geonames.org/*|/.*.rdf*": lambda x: load_uri_using_path(
            x, place.E53_PlaceFromGeonames
        ),
        "http://www.wikidata.org/*|/.*.rdf": lambda x: load_uri_using_path(
            x, place.E53_PlaceFromWikidata
        ),
    }

    @classmethod
    def get_rdf_types(cls):
        return [CRM.E53_Place]

    @classmethod
    def create_from_string(cls, string):
        return cls.objects.create(label=string)


class E74_Group(Entity):
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
            x, group.E74_GroupFromDNB
        ),
        "http://www.wikidata.org/*|/.*.rdf": lambda x: load_uri_using_path(
            x, group.E74_GroupFromWikidata
        ),
    }

    @classmethod
    def get_rdf_types(cls):
        return [CRM.E74_Group]

    @classmethod
    def create_from_string(cls, string):
        return cls.objects.create(label=string)


class SimpleLabelEntity(SimpleLabelModel, Entity):
    class Meta(SimpleLabelModel.Meta):
        abstract = True
