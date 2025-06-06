import functools
import logging
import re
from collections import defaultdict

from django.conf import settings
from django.db.models.base import ModelBase
from django.db.models import Case, Q, When
from django.urls import NoReverseMatch, reverse

from apis_core.apis_metainfo.models import RootObject
from apis_core.utils.settings import apis_base_uri
from apis_core.relations.models import Relation
from apis_core.relations.utils import get_relation_targets_from_model

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
        if getattr(cls, "enable_facets", False):
            for ct in get_relation_targets_from_model(cls):
                facetname = "relation_to_" + ct.model
                rels = Relation.objects.filter(
                    Q(obj_content_type=ct.id, subj_object_id__in=queryset)
                    | Q(subj_content_type=ct.id, obj_object_id__in=queryset)
                )
                rels = rels.annotate(
                    target=Case(
                        When(**{"obj_content_type": ct.id, "then": "obj_object_id"}),
                        When(**{"subj_content_type": ct.id, "then": "subj_object_id"}),
                    )
                )
                related_ids = [x.target for x in rels]
                instances = ct.model_class().objects.filter(pk__in=related_ids)

                for obj in instances:
                    related_ids = [x for x in rels if x.target == obj.id]
                    facets[facetname][obj.id] = {
                        "name": str(obj),
                        "count": len(set(related_ids)),
                    }
        return facets


