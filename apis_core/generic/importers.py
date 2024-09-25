import json
import logging
import urllib
from functools import cache

from django.core.exceptions import ImproperlyConfigured

from apis_core.utils.normalize import clean_uri
from apis_core.utils.rdf import get_definition_and_attributes_from_uri

logger = logging.getLogger(__name__)


class GenericModelImporter:
    """
    A generic importer class
    It provides the standard methods for importing data from
    an URI and creating a model instance of it.
    By default it fetches a resource, first tries to parse it using
    our rdf parser, if that fails tries to parse it using json and
    then extracts the fields whose keys match the model field names.
    Projects can inherit from this class and override the default
    methods or simple write their own from scratch.
    """

    model = None
    import_uri = None

    def __init__(self, uri, model):
        self.model = model
        self.import_uri = self.clean_uri(uri)

    @property
    def get_uri(self):
        return self.import_uri

    def clean_uri(self, uri):
        return clean_uri(uri)

    @cache
    def request(self, uri):
        # we first try to use the RDF parser
        try:
            defn, data = get_definition_and_attributes_from_uri(uri, self.model)
            return data
        except Exception as e:
            logger.debug(e)
        # if everything else fails, try parsing json
        # if even that does not help, return an empty dict
        try:
            return json.loads(urllib.request.urlopen(uri).read())
        except Exception as e:
            logger.debug(e)
        return {}

    def mangle_data(self, data):
        return data

    def get_data(self, drop_unknown_fields=True):
        """
        fetch the data using the `request` method and
        mangle the data using the `mangle_data` method.
        If the `drop_unknown_fields` argument is true,
        remove all fields from the data dict that do not
        have an equivalent field in the model.
        """
        data = self.request(self.import_uri)
        data = self.mangle_data(data)
        if drop_unknown_fields:
            # we are dropping all fields that are not part of the model
            modelfields = [field.name for field in self.model._meta.fields]
            data = {key: data[key] for key in data if key in modelfields}
        if not data:
            raise ImproperlyConfigured(
                f"Could not import {self.import_uri}. Data fetched was: {data}"
            )
        return data

    def import_into_instance(self, instance, fields="__all__"):
        data = self.get_data()
        if fields == "__all__":
            fields = data.keys()
        for field in fields:
            if hasattr(instance, field) and field in data.keys():
                setattr(instance, field, data[field])
        instance.save()

    def create_instance(self):
        return self.model.objects.create(**self.get_data(drop_unknown_fields=True))
