from django.views.generic.detail import DetailView
from django_tables2 import SingleTableMixin
from django_tables2.tables import table_factory
from simple_history.utils import get_history_model_for_model

from apis_core.generic.helpers import first_member_match, module_paths

from .tables import HistoryGenericTable


class HistoryView(SingleTableMixin, DetailView):
    template_name = "history/history.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if contenttype := kwargs.get("contenttype"):
            self.model = get_history_model_for_model(contenttype.model_class())
            self.queryset = self.model.objects.filter(id=kwargs.get("pk"))

    def get_table_class(self):
        table_modules = module_paths(self.model, path="tables", suffix="HistoryTable")
        table_class = first_member_match(table_modules, HistoryGenericTable)
        return table_factory(self.model, table_class)
