import logging

import django_filters
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django_filters.filterset import FilterSet

from apis_core.collections.filters import CollectionsIncludeExcludeFilter
from apis_core.search.filters import SearchFilterByContenttype

from .forms import GenericFilterSetForm

logger = logging.getLogger(__name__)


class GenericFilterSet(FilterSet):
    """
    Our GenericFilterSet sets the default `form` to be our
    GenericFilterSetForm, which is set up to ignore the `columns` field
    of the form.
    """

    class Meta:
        form = GenericFilterSetForm
        # we set the UnknownFieldBehavior to WARN, so the form does not
        # break if there are JSONFields
        unknown_field_behavior = django_filters.UnknownFieldBehavior.WARN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = self._meta.model
        # remove all the filters that are based on auto_created model fields
        for field in model._meta.get_fields():
            if getattr(field, "auto_created", False) and field.name in self.filters:
                del self.filters[field.name]
        if apps.is_installed("apis_core.search"):
            searchmodel = apps.get_model("search", "SearchEntry")
            content_type = ContentType.objects.get_for_model(model)
            if searchmodel.objects.filter(content_type=content_type).exists():
                self.filters["search"] = SearchFilterByContenttype(
                    content_type=content_type, object_id_field="pk"
                )

        try:
            skoscollection = apps.get_model("collections.SkosCollection")
            if skoscollection.objects.exists():
                self.filters["collections"] = CollectionsIncludeExcludeFilter(
                    queryset=skoscollection.objects.all(),
                )
        except LookupError as e:
            logger.debug("Not adding collections filter to form: %s", e)
