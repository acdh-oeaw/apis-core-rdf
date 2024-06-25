import json
import urllib
from django.core.exceptions import ImproperlyConfigured
from apis_core.utils.normalize import clean_uri


class GenericModelImporter:
    """
    A generic importer class
    It provides the standard methods for importing data from
    an URI and creating a model instance of it.
    By default it fetches a resource, tries to parse it using json and
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

    def request(self, uri):
        try:
            return json.loads(urllib.request.urlopen(uri).read())
        except Exception:
            return {}

    def mangle_data(self, data):
        return data

    def create_instance(self):
        data = self.request(self.import_uri)
        data = self.mangle_data(data)
        # we are dropping all fields that are not part of the model
        modelfields = [field.name for field in self.model._meta.fields]
        fielddata = {key: data[key] for key in data if key in modelfields}
        if fielddata:
            return self.model.objects.create(**fielddata)
        raise ImproperlyConfigured(
            f"Could not import {self.import_uri}. Data fetched was: {data}"
        )
