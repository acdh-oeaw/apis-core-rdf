from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
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
