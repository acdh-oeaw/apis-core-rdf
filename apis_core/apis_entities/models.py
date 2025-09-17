import functools
import logging
import re
from collections import Counter, defaultdict

from django.conf import settings
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Case, CharField, F, Q, Value, When
from django.db.models.base import ModelBase
from django.db.models.functions import Coalesce, Concat
from django.db.models.sql.query import OuterRef
from django.urls import NoReverseMatch, reverse

from apis_core.apis_metainfo.models import RootObject
from apis_core.relations.models import Relation
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
    def annotate_with_facets(cls, queryset):
        """Annotate the queryset with facets."""
        rels = (
            Relation.objects.filter(
                Q(obj_object_id=OuterRef("id")) | Q(subj_object_id=OuterRef("id"))
            )
            .annotate(
                _facet=Case(
                    When(obj_object_id=OuterRef("id"), then=F("subj_object_id")),
                    default=F("obj_object_id"),
                )
            )
            .values_list("_facet", flat=True)
        )
        queryset = queryset.annotate(facets=ArraySubquery(rels))
        return queryset

    @staticmethod
    def create_when_clause_for_entity(entity_cls):
        res = {f"{entity_cls.__name__.lower()}__isnull": False}
        label = getattr(entity_cls, "facet_label", None)
        if not label:
            return When(
                **res,
                then=Concat(Value("no label, id: "), F("id"), output_field=CharField()),
            )
        elif isinstance(label, list):
            return When(
                **res,
                then=Coalesce(
                    *label,
                    default=Concat(
                        Value("no label, id: "), F("id"), output_field=CharField()
                    ),
                ),
            )
        elif isinstance(label, str):
            return When(
                **res,
                then=Coalesce(
                    F(f"{entity_cls.__name__.lower()}__{label}"),
                    Value("no label"),
                    default=Concat(
                        Value("no label, id: "), F("id"), output_field=CharField()
                    ),
                ),
            )
        else:
            raise ValueError(f"Invalid facet label type for {entity_cls}")

    @classmethod
    def get_facets(cls, queryset, top=None):
        facets = defaultdict(dict)
        if getattr(cls, "enable_facets", False):
            from apis_core.apis_entities.utils import get_entity_classes

            queryset = cls.annotate_with_facets(queryset)
            all_facets = []
            for facet_array in queryset.values_list("facets", flat=True):
                all_facets.extend(facet_array)
            when_clauses_entities = [
                cls.create_when_clause_for_entity(entity_cls)
                for entity_cls in get_entity_classes()
            ]
            when_clauses_classes = [
                When(
                    **{f"{cls.__name__.lower()}__isnull": False},
                    then=Value(cls.__name__),
                )
                for cls in get_entity_classes()
            ]
            facet_data = (
                RootObject.objects_inheritance.filter(id__in=set(all_facets))
                .annotate(
                    label_facet=Case(
                        *when_clauses_entities,
                        default=Concat(
                            Value("ID: "), Value("test"), output_field=CharField()
                        ),
                    ),
                    label_class=Case(
                        *when_clauses_classes,
                        default=Value("Unknown"),
                    ),
                )
                .values("id", "label_facet", "label_class")
            )

            facet_dict = {
                item["id"]: (item["label_facet"], item["label_class"])
                for item in facet_data
            }

            counter = Counter(all_facets)
            for facet, count in counter.most_common(top):
                if facet in facet_dict:
                    label_facet, label_class = facet_dict[facet]
                    facets[label_class][label_facet] = count

        return facets
