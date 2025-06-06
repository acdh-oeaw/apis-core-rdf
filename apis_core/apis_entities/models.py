import functools
import logging
import re
from collections import defaultdict

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Case, CharField, F, Q, Value, When
from django.db.models.base import ModelBase
from django.db.models.functions import Concat
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
    def get_facet_label(cls):
        if "db_string" in cls._meta.get_fields():
            return F("db_string")
        return Concat(
            Value(f"{cls._meta.verbose_name.title()} "),
            F("pk"),
            output_field=CharField(),
        )

    @classmethod
    def get_facets(cls, queryset):
        facets = defaultdict(dict)
        if getattr(cls, "enable_facets", False):
            my_content_type = ContentType.objects.get_for_model(queryset.model)

            # we filter all the relations that are somehow connected to instances of this queryset
            # we are only interested in the id and the type of the object the relations point to,
            # so we store those in `target_id` and `target_content_type`
            query_filter = Q(
                subj_content_type=my_content_type, subj_object_id__in=queryset
            ) | Q(
                Q(obj_content_type=my_content_type, obj_object_id__in=queryset),
                ~Q(subj_content_type=my_content_type),
            )
            rels = (
                Relation.objects.to_content_type_with_targets(my_content_type).values(
                    "target_id", "target_content_type"
                )
            ).filter(query_filter)

            # we use the ids to get a the labels of the targets
            # and we store those in an id: label dict
            target_ids = [rel["target_id"] for rel in rels]
            entity_classes = list(
                filter(lambda x: issubclass(x, AbstractEntity), apps.get_models())
            )

            # this should be moved to an EntityManager once the entites app is in apis_core
            when_clauses_classes = [
                When(
                    **{f"{cls.__name__.lower()}__isnull": False},
                    then=cls.get_facet_label(),
                )
                for cls in entity_classes
            ]
            identifiers = (
                RootObject.objects_inheritance.filter(id__in=target_ids)
                .select_subclasses()
                .annotate(label=Case(*when_clauses_classes))
                .values("pk", "label")
            )

            identifiers = {item["pk"]: item["label"] for item in identifiers}

            for rel in rels:
                _id = rel["target_id"]
                content_type = rel["target_content_type"]
                facetname = (
                    "relation_to_" + ContentType.objects.get_for_id(content_type).name
                )
                if _id in facets[facetname]:
                    facets[facetname][_id]["count"] += 1
                else:
                    facets[facetname][_id] = {
                        "count": 1,
                        "name": identifiers.get(_id, "Unknown"),
                    }
        return facets
