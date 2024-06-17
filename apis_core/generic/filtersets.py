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

    class Meta:
        form = GenericFilterSetForm

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
