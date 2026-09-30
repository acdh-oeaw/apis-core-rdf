from django.db.models import Exists, OuterRef
from django_filters import CharFilter

from .models import SearchEntry


class SearchFilter(CharFilter):
    """
    Custom CharFilter that uses the search lookup to return a
    Queryset that only contains instances that also exist in
    a search for `value` over SearchEntries.

    :param content_type_field:  The name of the field that should be compared
    to the `SearchEntry.content_type` field
    :param object_id_field: The name of the field that should be compared to
    the `SearchEntry.object_id` field
    """

    def __init__(self, content_type_field: str, object_id_field: str, *args, **kwargs):
        self.content_type_field = content_type_field
        self.object_id_field = object_id_field
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            search_entry_qs = SearchEntry.objects.search(value)
            res = qs.filter(
                Exists(
                    search_entry_qs.filter(
                        content_type_id=OuterRef(self.content_type_field),
                        object_id=OuterRef(self.object_id_field),
                    )
                )
            )
            return res
        return qs


class SearchFilterByContenttype(CharFilter):
    """
    Custom CharFilter that uses the search lookup in combination
    with a content type to return a Queryset that only contains
    instances from that content type that also exist in a search
    for `value` over SearchEntries

    :param content_type: The natural key of the content type that the
    `SearchEntry` queryset should be filtered for
    :param object_id_field:  The name of the field that should be compared to
    the `SearchEntry.object_id` field
    """

    def __init__(self, content_type: str, object_id_field: str, *args, **kwargs):
        self.content_type = content_type
        self.object_id_field = object_id_field
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            search_entry_qs = SearchEntry.objects.search(
                value, content_types=[self.content_type]
            )
            res = qs.filter(
                Exists(
                    search_entry_qs.filter(
                        object_id=OuterRef(self.object_id_field),
                    )
                )
            )
            return res
        return qs
