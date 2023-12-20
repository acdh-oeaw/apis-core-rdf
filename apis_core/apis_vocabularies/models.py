import re
import unicodedata

from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from apis_core.apis_metainfo.models import RootObject


class VocabNames(models.Model):
    """List of Vocabulary names to allow the easy retrieval\
    of Vovcabulary names and classes from the VocabsBaseClass"""

    name = models.CharField(max_length=255)

    def get_vocab_label(self):
        return re.sub(r"([A-Z])", r" \1", self.name).strip()


# TODO RDF: Remove VocabsBaseClass entirely


class VocabsBaseClass(RootObject):
    """An abstract base class for other classes which contain so called
    'controlled vocabulary' to describe subtypes of main temporalized
    entites"""

    choices_status = (
        ("rej", "rejected"),
        ("ac", "accepted"),
        ("can", "candidate"),
        ("del", "deleted"),
    )
    description = models.TextField(
        blank=True, help_text="Brief description of the used term."
    )
    parent_class = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE
    )
    status = models.CharField(max_length=4, choices=choices_status, default="can")
    userAdded = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )
    vocab_name = models.ForeignKey(
        VocabNames, blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        d, created = VocabNames.objects.get_or_create(name=type(self).__name__)
        self.vocab_name = d
        if self.name != unicodedata.normalize(
            "NFC", self.name
        ):  # secure correct unicode encoding
            self.name = unicodedata.normalize("NFC", self.name)
        super(VocabsBaseClass, self).save(*args, **kwargs)
        return self

    @cached_property
    def label(self):
        d = self
        res = self.name
        while d.parent_class:
            res = d.parent_class.name + " >> " + res
            d = d.parent_class
        return res


class VocabsUri(models.Model):
    """Class to store URIs for imported types. URI class from metainfo is not
    used in order to keep the vocabularies module/app seperated from the rest of the application.
    """

    uri = models.URLField()
    domain = models.CharField(max_length=255, blank=True)
    rdf_link = models.URLField(blank=True)
    vocab = models.ForeignKey(
        VocabsBaseClass, blank=True, null=True, on_delete=models.CASCADE
    )
    # loaded: set to True when RDF was loaded and parsed into the data model
    loaded = models.BooleanField(default=False)
    # loaded_time: Timestamp when file was loaded and parsed
    loaded_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.uri


# TODO RDF: Check if this should be removed or adapted
#
# @reversion.register(follow=['vocabsbaseclass_ptr'])
# class WorkType(VocabsBaseClass):
#     """Holds controlled vocabularies about work-types"""
#     pass
#
#
# @reversion.register(follow=['vocabsbaseclass_ptr'])
# class Title(VocabsBaseClass):
#     """A person´s (academic) title"""
#     abbreviation = models.CharField(max_length=10, blank=True)
#
#
# @reversion.register(follow=['vocabsbaseclass_ptr'])
# class ProfessionType(VocabsBaseClass):
#     """Holds controlled vocabularies about profession-types"""
#     pass
#
#
# @reversion.register(follow=['vocabsbaseclass_ptr'])
# class PlaceType(VocabsBaseClass):
#     """Holds controlled vocabularies about place-types"""
#     pass
#
#
# @reversion.register(follow=['vocabsbaseclass_ptr'])
# class InstitutionType(VocabsBaseClass):
#     """Holds controlled vocabularies about institution-types"""
#     pass
#
#
# @reversion.register(follow=['vocabsbaseclass_ptr'])
# class EventType(VocabsBaseClass):
#     """Holds controlled vocabularies about event-types"""
#     pass


# TODO RDF: Remove this
class CollectionType(VocabsBaseClass):
    """e.g. reseachCollection, importCollection"""

    pass
