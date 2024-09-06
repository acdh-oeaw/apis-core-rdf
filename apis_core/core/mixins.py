from django.conf import settings
from django.contrib.auth.mixins import AccessMixin

from apis_core.utils.utils import access_for_all


class ViewPassesTestMixin(AccessMixin):
    """
    Deny a request with a permission error if the test_func() method returns
    False. This is mostly a copy of Django's UserPassesTestMixin, but it allows
    to set the APIS_VIEW_PASSES_TEST setting to define a function that receives
    the view and can perform checks on any of the views attributes.
    If such a setting does not exist, it falls back  to APIS' access_for_all
    function.
    """

    def test_func(self):
        if hasattr(settings, "APIS_VIEW_PASSES_TEST"):
            return settings.APIS_VIEW_PASSES_TEST(self)
        # fall back to more general access check
        return access_for_all(self, viewtype="detail")

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        view_test_result = self.get_test_func()()
        if not view_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


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
