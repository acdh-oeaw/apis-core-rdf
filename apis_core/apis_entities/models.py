import functools
import logging
import re
from collections import defaultdict

from django.conf import settings
from django.db.models import Case, Q, When
from django.db.models.base import ModelBase
from django.urls import NoReverseMatch, reverse
from django.contrib.contenttypes.models import ContentType

from apis_core.apis_metainfo.models import RootObject
from apis_core.relations.models import Relation
from apis_core.relations.utils import get_relation_targets_from_model
from apis_core.utils.settings import apis_base_uri

NEXT_PREV = getattr(settings, "APIS_NEXT_PREV", True)

logger = logging.getLogger(__name__)


class AbstractEntityModelBase(ModelBase):
    def __new__(metacls, name, bases, attrs):
        if name == "AbstractEntity":
            return super().__new__(metacls, name, bases, attrs)
        else:
            new_class = super().__new__(metacls, name, bases, attrs)
            if not new_class._meta.ordering:
                logger.warning(
                    f"{name} inherits from AbstractEntity but does not specify 'ordering' in its Meta class. "
                    "Empty ordering could result in inconsitent results with pagination. "
                    "Set a ordering or inherit the Meta class from AbstractEntity.",
                )

            return new_class


class AbstractEntity(RootObject, metaclass=AbstractEntityModelBase):
    """
    Abstract super class which encapsulates common logic between the
    different entity kinds and provides various methods relating to either
    all or one specific entity kind.

    Most of the class methods are designed to be used in the subclass as they
    are considering contexts which depend on the subclass entity type.
    So they are to be understood in that dynamic context.
    """

    class Meta:
        abstract = True

    @classmethod
    def get_or_create_uri(cls, uri):
        uri = str(uri)
        try:
            if re.match(r"^[0-9]*$", uri):
                p = cls.objects.get(pk=uri)
            else:
                p = cls.objects.get(uri__uri=uri)
            return p
        except Exception as e:
            print("Found no object corresponding to given uri." + e)
            return False

    # TODO
    @classmethod
    def get_entity_list_filter(cls):
        return None

    @functools.cached_property
    def get_prev_id(self):
        if NEXT_PREV:
            prev_instance = (
                type(self)
                .objects.filter(id__lt=self.id)
                .order_by("-id")
                .only("id")
                .first()
            )
            if prev_instance is not None:
                return prev_instance.id
        return False

    @functools.cached_property
    def get_next_id(self):
        if NEXT_PREV:
            next_instance = (
                type(self)
                .objects.filter(id__gt=self.id)
                .order_by("id")
                .only("id")
                .first()
            )
            if next_instance is not None:
                return next_instance.id
        return False

    def get_default_uri(self):
        try:
            route = reverse("GetEntityGenericRoot", kwargs={"pk": self.pk})
        except NoReverseMatch:
            route = reverse("apis_core:GetEntityGeneric", kwargs={"pk": self.pk})
        base = apis_base_uri().strip("/")
        return f"{base}{route}"

    @classmethod
    def get_facets(cls, queryset):
        facets = defaultdict(dict)
        if getattr(cls, "enable_facets", True):
            my_content_type = ContentType.objects.get_for_model(queryset.model)
            query_filter = Q(subj_content_type=my_content_type, subj_object_id__in=queryset) | Q(obj_content_type=my_content_type, obj_object_id__in=queryset)
            rels = Relation.objects.filter(query_filter).annotate(
                    target_content_type=Case(When(**{"subj_content_type": my_content_type, "then": "obj_content_type"}), default="subj_content_type"),
                    target_id=Case(When(**{"subj_content_type": my_content_type, "then": "obj_object_id"}), default="subj_object_id")
            )
            target_ids = rels.values_list("target_id", flat=True)
            identifiers = RootObject.objects_inheritance.filter(id__in=target_ids).select_subclasses()
            identifiers = {item.pk: str(item) for item in identifiers}

            for rel in rels:
                facetname = "relation_to_" + ContentType.objects.get(pk=rel.target_content_type).name
                if rel.target_id in facets[facetname]:
                    facets[facetname][rel.target_id]["count"] += 1
                else:
                    facets[facetname][rel.target_id] = {"count": 1, "name": identifiers[rel.target_id]}
        return facets
