import logging

import django_filters
from django.apps import apps
from django_filters.filterset import FilterSet

from apis_core.collections.filters import CollectionsIncludeExcludeFilter

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
        try:
            skoscollection = apps.get_model("collections.SkosCollection")
            if skoscollection.objects.exists():
                self.filters["collections"] = CollectionsIncludeExcludeFilter(
                    queryset=skoscollection.objects.all(),
                )
        except LookupError as e:
            logger.debug("Not adding collections filter to form: %s", e)
