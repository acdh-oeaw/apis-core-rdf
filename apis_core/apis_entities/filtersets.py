import django_filters
from django.db import models
from django.db.models import Q, Case, When
from apis_core.generic.filtersets import GenericFilterSet, GenericFilterSetForm
from apis_core.apis_relations.models import Property, Triple
from apis_core.generic.helpers import generate_search_filter
from apis_core.apis_entities.utils import get_entity_classes
from apis_core.apis_metainfo.models import RootObject

ABSTRACT_ENTITY_COLUMNS_EXCLUDE = [
    "rootobject_ptr",
    "self_contenttype",
]

ABSTRACT_ENTITY_FILTERS_EXCLUDE = ABSTRACT_ENTITY_COLUMNS_EXCLUDE + [
    "review",
    "start_date",
    "start_start_date",
    "start_end_date",
    "end_date",
    "end_start_date",
    "end_end_date",
    "notes",
    "text",
    "published",
    "status",
    "references",
]


def related_property(queryset, name, value):
    p = Property.objects.get(name_forward=value)
    queryset = queryset.filter(triple_set_from_subj__prop=p).distinct()
    return queryset


def related_entity(queryset, name, value):
    entities = get_entity_classes()
    q = Q()
    for entity in entities:
        name = entity._meta.model_name
        q |= Q(**{f"{name}__isnull": False}) & generate_search_filter(
            entity, value, prefix=f"{name}__"
        )
    all_entities = RootObject.objects_inheritance.filter(q).values_list("pk", flat=True)
    t = (
        Triple.objects.filter(Q(subj__in=all_entities) | Q(obj__in=all_entities))
        .annotate(
            related=Case(
                When(subj__in=all_entities, then="obj"),
                When(obj__in=all_entities, then="subj"),
            )
        )
        .values_list("related", flat=True)
    )
    return queryset.filter(pk__in=t)


class AbstractEntityFilterSetForm(GenericFilterSetForm):
    columns_exclude = ABSTRACT_ENTITY_COLUMNS_EXCLUDE


class AbstractEntityFilterSet(GenericFilterSet):
    related_entity = django_filters.CharFilter(
        method=related_entity, label="Related entity contains"
    )
    related_property = django_filters.ModelChoiceFilter(
        queryset=Property.objects.all().order_by("name_forward"),
        label="Related Property",
        method=related_property,
    )

    class Meta(GenericFilterSet.Meta):
        form = AbstractEntityFilterSetForm
        exclude = ABSTRACT_ENTITY_FILTERS_EXCLUDE
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }
