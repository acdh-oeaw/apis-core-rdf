from django.forms import Form
from django.views.generic.detail import BaseDetailView, DetailView
from django.views.generic.edit import FormView
from django_tables2 import SingleTableMixin
from django_tables2.tables import table_factory

from apis_core.generic.helpers import first_member_match, module_paths
from apis_core.generic.views import GenericModelMixin

from .tables import HistoryGenericTable


class HistoryView(GenericModelMixin, SingleTableMixin, DetailView):
    template_name = "history/history.html"

    def get_table_class(self):
        table_modules = module_paths(self.model, path="tables", suffix="HistoryTable")
        table_class = first_member_match(table_modules, HistoryGenericTable)
        return table_factory(self.model, table_class)

    def get_table_data(self):
        return self.get_object().get_history_data()


class HistoryReset(GenericModelMixin, BaseDetailView, FormView):
    form_class = Form
    template_name = "history/reset.html"

    def form_valid(self, form):
        self.get_object().instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_object().instance.get_history_url()
