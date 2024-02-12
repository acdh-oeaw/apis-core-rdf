import django_filters
from django.db import models
from apis_core.generic.filtersets import GenericFilterSet, GenericFilterSetForm
from apis_core.utils.filtermethods import related_entity_name
from apis_core.apis_relations.models import Property

ABSTRACT_ENTITY_FILTERS_EXCLUDE = [
    "rootobject_ptr",
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


def related_property(queryset, name, value):
    p = Property.objects.get(deprecated_name=value)
    queryset = queryset.filter(triple_set_from_subj__prop=p).distinct()
    return queryset


class AbstractEntityFilterSetForm(GenericFilterSetForm):
    columns_exclude = ABSTRACT_ENTITY_FILTERS_EXCLUDE


class AbstractEntityFilterSet(GenericFilterSet):
    related_entity_name = django_filters.CharFilter(
        method=related_entity_name, label="Related entity"
    )
    related_property = django_filters.ModelChoiceFilter(
        queryset=Property.objects.all().order_by("deprecated_name"),
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
