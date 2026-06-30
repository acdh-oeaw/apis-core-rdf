import functools

import django_filters
from django.contrib.contenttypes.models import ContentType

from apis_core.generic.filtersets import GenericFilterSet

from .models import Uri


@functools.cache
def content_type_ids() -> list[int]:
    return Uri.objects.all().values("content_type").distinct()


class UriFilterSet(GenericFilterSet):
    uri = django_filters.CharFilter(lookup_expr="icontains")
    content_type = django_filters.ModelMultipleChoiceFilter(
        queryset=ContentType.objects.filter(pk__in=content_type_ids())
    )
