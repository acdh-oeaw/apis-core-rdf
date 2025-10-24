from django.forms import Form
from django.views.generic.detail import BaseDetailView, DetailView
from django.views.generic.edit import FormView
from django_tables2 import SingleTableMixin
from django_tables2.tables import table_factory

from apis_core.generic.helpers import first_member_match, module_paths
from apis_core.generic.views import (
    GenericModelMixin,
    GenericModelPermissionRequiredMixin,
)

from .tables import HistoryGenericTable


class HistoryView(
    GenericModelMixin, GenericModelPermissionRequiredMixin, SingleTableMixin, DetailView
):
    """
    This view lists the historical data of one object.
    The `GenericModel` this view acts upon is NOT the historical model, but the base model.
    I.e. it is not the `VersionPerson`, but the `Person`. Therefore the permission required
    to access this view refers to the `Person` model, NOT the `VersionPerson` model!
    """

    template_name = "history/history.html"
    permission_action_required = "view"

    def get_table_class(self):
        table_modules = module_paths(self.model, path="tables", suffix="HistoryTable")
        table_class = first_member_match(table_modules, HistoryGenericTable)
        return table_factory(self.model, table_class)

    def get_table_data(self):
        return self.get_object().get_history_data()


class HistoryReset(
    GenericModelMixin, GenericModelPermissionRequiredMixin, BaseDetailView, FormView
):
    """
    This view allows to reset a model instance to an earlier version.
    The `GenericModel` this view acts upon IS the historical model, so the permission
    required to access the view refers to the versioned model. For example for the
    `Person` model, this view acts upon the `VersionPerson` model and therefore the
    permission required is the `.versionperson_view` permission.
    """

    form_class = Form
    template_name = "history/reset.html"
    permission_action_required = "change"

    def form_valid(self, form):
        self.get_object().instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_object().instance.get_history_url()
