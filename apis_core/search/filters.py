from django_filters import CharFilter
from .models import SearchEntry


class SearchFilter(CharFilter):
    """
    Custom CharFilter that uses the search lookup to return a
    Queryset that matches the filter string.
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            res = qs.filter(**{f"{self.field_name}__in": SearchEntry.objects.search(value, self.content_types)})
        return qs

