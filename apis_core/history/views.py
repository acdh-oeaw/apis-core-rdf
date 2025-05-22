from django.views.generic.detail import DetailView
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
