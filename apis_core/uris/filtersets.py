import django_filters

from apis_core.generic.filtersets import GenericFilterSet


class UriFilterSet(GenericFilterSet):
    uri = django_filters.CharFilter(lookup_expr="icontains")
