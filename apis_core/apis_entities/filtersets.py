import django_filters
from django.apps import apps
from django.conf import settings
from django.db import models
from django.forms import DateInput
from django.utils.encoding import force_str
from simple_history.utils import get_history_manager_for_model

from apis_core.generic.filtersets import GenericFilterSet
from apis_core.generic.helpers import default_search_fields, generate_search_filter


class ModelSearchFilter(django_filters.CharFilter):
    """
    This filter is a customized CharFilter that
    uses the `generate_search_filter` method to
    adapt the search filter to the model that is
    searched.
    It also extracts sets the help text based on
    the fields searched.
    """

    def __init__(self, *args, **kwargs):
        model = kwargs.pop("model", None)
        super().__init__(*args, **kwargs)

        if model is not None and "help_text" not in self.extra:
            field_names = [field.verbose_name for field in default_search_fields(model)]
            # use force_str on the fields verbose names to convert
            # lazy instances to string and join the results
            fields = ", ".join(map(force_str, field_names))
            self.extra["help_text"] = f"Search in fields: {fields}"

    def filter(self, qs, value):
        return qs.filter(generate_search_filter(qs.model, value))


def changed_since(queryset, name, value):
    history = get_history_manager_for_model(queryset.model)
    ids = history.filter(history_date__gt=value).values_list("id", flat=True)
    return queryset.filter(pk__in=ids)


class AbstractEntityFilterSet(GenericFilterSet):
    class Meta(GenericFilterSet.Meta):
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if model := getattr(self.Meta, "model", False):
            self.filters["search"] = ModelSearchFilter(model=model)
            self.filters.move_to_end("search", False)

        if "apis_core.history" in settings.INSTALLED_APPS:
            self.filters["changed_since"] = django_filters.DateFilter(
                label="Changed since",
                widget=DateInput(attrs={"type": "date"}),
                method=changed_since,
            )

        if apps.is_installed("apis_core.relations"):
            from apis_core.relations.filters import RelationFilter

            self.filters["relation"] = RelationFilter()
