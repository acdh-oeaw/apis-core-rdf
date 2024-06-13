from django_filters.filterset import FilterSet

from .forms import GenericFilterSetForm


class GenericFilterSet(FilterSet):
    """
    Our GenericFilterSet sets the default `form` to be our
    GenericFilterSetForm, which is set up to ignore the `columns` field
    of the form.
    """

    class Meta:
        form = GenericFilterSetForm
