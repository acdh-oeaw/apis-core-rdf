from django_filters.constants import ALL_FIELDS
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


# This is a backport from https://github.com/carltongibson/django-filter/pull/1636
# It can be removed once that is merged and released
def filterset_factory(model, filterset=FilterSet, fields=ALL_FIELDS):
    attrs = {"model": model, "fields": fields}
    bases = (filterset.Meta,) if hasattr(filterset, "Meta") else ()
    Meta = type("Meta", bases, attrs)
    return type(filterset)(
        str("%sFilterSet" % model._meta.object_name), (filterset,), {"Meta": Meta}
    )
