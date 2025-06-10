import json
import logging
import urllib
from functools import cache

from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import IntegrityError

from apis_core.apis_metainfo.models import Uri
from apis_core.apis_metainfo.utils import create_object_from_uri
from apis_core.utils.rdf import get_something_from_uri

logger = logging.getLogger(__name__)


class GenericModelImporter:
    """
    A generic importer class which provides methods for
    importing data from a URI and creating a model instance from it.

    By default, it fetches a resource and first tries to parse it using
    our RDF parser. If that fails, it tries to parse it using JSON and
    then extracts the fields whose keys match the model field names.
    Projects can inherit from this class and override the default
    methods or simply write their own from scratch.
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
        return get_normalized_uri(uri)

    @cache
    def request(self, uri):
        # we first try to use the RDF parser
        try:
            data = get_something_from_uri(
                uri,
                [self.model],
            )
            return data
        except Exception as e:
            logger.debug(e)
        # if everything else fails, try parsing JSON
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
        Fetch the data using the `request` method and
        mangle it using the `mangle_data` method.

        If the `drop_unknown_fields` argument is True,
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
                setattr(instance, field, data[field][0])
        instance.save()

    def create_instance(self):
        logger.debug("Create instance from URI %s", self.import_uri)
        data = self.get_data(drop_unknown_fields=False)
        instance = None
        same_as = data.get("same_as", [])
        same_as = [get_normalized_uri(uri) for uri in same_as]
        if sa := Uri.objects.filter(uri__in=same_as):
            root_set = set([s.content_object for s in sa])
            if len(root_set) > 1:
                raise IntegrityError(
                    f"Multiple objects found for sameAs URIs {data['same_as']}. "
                    f"This indicates a data integrity problem as these URIs should be unique."
                )
            instance = sa.first().content_object
            logger.debug("Found existing instance %s", instance)
        if not instance:
            attributes = {}
            for field in self.model._meta.fields:
                if data.get(field.name, False):
                    attributes[field.name] = data[field.name][0]
            instance = self.model.objects.create(**attributes)
            logger.debug("Created instance %s from attributes %s", instance, attributes)
        content_type = ContentType.objects.get_for_model(instance)
        for uri in same_as:
            Uri.objects.get_or_create(
                uri=uri, content_type=content_type, object_id=instance.id
            )
        for relation, details in data.get("relations", {}).items():
            rel_app_label, rel_model = relation.split(".")
            relation_model = ContentType.objects.get_by_natural_key(
                app_label=rel_app_label, model=rel_model
            ).model_class()

            reld = details.get("obj", None) or details.get("subj", None)
            reld_app_label, reld_model = reld.split(".")
            related_content_type = ContentType.objects.get_by_natural_key(
                app_label=reld_app_label, model=reld_model
            )
            related_model = related_content_type.model_class()

            for related_uri in details["curies"]:
                try:
                    related_instance = create_object_from_uri(
                        uri=related_uri, model=related_model
                    )
                    if details.get("obj"):
                        subj_object_id = instance.pk
                        subj_content_type = content_type
                        obj_object_id = related_instance.pk
                        obj_content_type = related_content_type
                    else:
                        obj_object_id = instance.pk
                        obj_content_type = content_type
                        subj_object_id = related_instance.pk
                        subj_content_type = related_content_type
                    rel, _ = relation_model.objects.get_or_create(
                        subj_object_id=subj_object_id,
                        subj_content_type=subj_content_type,
                        obj_object_id=obj_object_id,
                        obj_content_type=obj_content_type,
                    )
                    logger.debug(
                        "Created relation %s between %s and %s",
                        relation_model.name(),
                        rel.subj,
                        rel.obj,
                    )
                except Exception as e:
                    logger.error(
                        "Could not create relation to %s due to %s", related_uri, e
                    )
        return instance
