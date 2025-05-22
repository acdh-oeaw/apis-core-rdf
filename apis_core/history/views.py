from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
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


def create_new_version(request, contenttype, pk):
    """Gets the version of the history instance and creates a new version."""
    model = contenttype.model_class()
    instance = model.objects.get(id=pk)
    history_latest = instance.history.latest()
    history_latest.history_id = None
    history_latest.history_date = timezone.now()
    history_latest.save()
    return redirect(
        reverse(
            "apis_core:generic:detail",
            args=[
                ContentType.objects.get_for_model(history_latest.__class__),
                history_latest.history_id,
            ],
        )
    )
