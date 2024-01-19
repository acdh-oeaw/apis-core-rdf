import django_filters
from apis_core.generic.filtersets import GenericFilterSet, GenericFilterSetForm

from apis_core.utils.filtermethods import (
    related_entity_name,
    related_property_name,
)

ABSTRACT_ENTITY_FILTERS_EXCLUDE = [
    "self_contenttype",
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


class bAbstractEntityFilterSet(GenericFilterSet):
    related_entity_name = django_filters.CharFilter(
        method=related_entity_name, label="Related entity"
    )
    related_property_name = django_filters.CharFilter(
        method=related_property_name, label="Related property"
    )

    class Meta:
        form = GenericFilterSetForm
        exclude = ABSTRACT_ENTITY_FILTERS_EXCLUDE
