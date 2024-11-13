from django.conf import settings


class ListViewObjectFilterMixin:
    """
    Filter a queryset of a listview using the APIS_LIST_VIEW_OBJECT_FILTER
    setting if it exists. A child class has to call the `filter_queryset`
    method somewhere, most likely in the `get_queryset` method.
    """

    def filter_queryset(self, queryset):
        if hasattr(super(), "filter_queryset"):
            queryset = super().filter_queryset(queryset)
        if hasattr(settings, "APIS_LIST_VIEW_OBJECT_FILTER"):
            return settings.APIS_LIST_VIEW_OBJECT_FILTER(self, queryset)
        return queryset

    def get_permission_required(self):
        if getattr(settings, "APIS_LIST_VIEWS_ALLOWED", False):
            return []
        return super().get_permission_required()
