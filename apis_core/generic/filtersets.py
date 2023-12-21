from django_filters.filterset import FilterSet
from .forms import GenericFilterSetForm


class GenericFilterSet(FilterSet):
    """
    This is a workaround because the FilterSet class of django-filters
    does not allow passing form arguments to the form - but we want to
    pass the `model` to the form, so we can create the `columns` form
    field.
    See also: https://github.com/carltongibson/django-filter/issues/1630
    """

    @property
    def form(self):
        if not hasattr(self, "_form"):
            Form = self.get_form_class()
            if self.is_bound:
                self._form = Form(
                    self.data, prefix=self.form_prefix, model=self._meta.model
                )
            else:
                self._form = Form(prefix=self.form_prefix, model=self._meta.model)
        return self._form


def filterset_factory(model, filterset=GenericFilterSet, fields="__all__"):
    """
    A custom filterset_factory, because we want to be a able to set the
    filterset as well as the `form` attribute of the filterset
    This can hopefully be removed once
    https://github.com/carltongibson/django-filter/issues/1631 is implemented.
    """

    meta = type(
        str("Meta"),
        (object,),
        {"model": model, "fields": fields, "form": GenericFilterSetForm},
    )
    filterset = type(
        str("%sFilterSet" % model._meta.object_name),
        (filterset,),
        {"Meta": meta},
    )
    return filterset
