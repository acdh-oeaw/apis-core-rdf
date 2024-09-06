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
    latest_version_list = [
        int(x.replace("v", ""))
        for x in instance.history.filter(version_tag__isnull=False).values_list(
            "version_tag", flat=True
        )
    ]
    history_latest.history_id = None
    history_latest.history_date = timezone.now()
    history_latest.save()
    if latest_version_list:
        latest_version = max(latest_version_list)
    else:
        latest_version = 0
    history_latest.set_version_tag(f"v{latest_version + 1}")
    return redirect(
        reverse(
            "apis_core:generic:detail",
            args=[
                ContentType.objects.get_for_model(history_latest.__class__),
                history_latest.history_id,
            ],
        )
    )
