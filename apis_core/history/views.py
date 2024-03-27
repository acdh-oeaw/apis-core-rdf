from apis_core.generic.views import GenericModelMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from django.views.generic.detail import SingleObjectMixin


def convert_timestamps(data):
    for key, value in data.items():
        if isinstance(value, str):
            try:
                timestamp = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
                data[key] = timestamp.strftime("%d.%m.%Y %H:%M")
            except ValueError:
                continue
        elif isinstance(value, dict):
            data[key] = convert_timestamps(value)
        elif isinstance(value, list):
            for i in range(len(value)):
                if isinstance(value[i], dict):
                    value[i] = convert_timestamps(value[i])
    return data


class ChangeHistoryView(GenericModelMixin, SingleObjectMixin, TemplateView):
    template_name = "history/change_history.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


def create_new_version(request, contenttype, pk):
    """Gets the version of the history instance and creates a new version."""
    historytripel_ids = request.GET.getlist("historytripel_ids")
    for ent in historytripel_ids:
        if "," in ent:
            historytripel_ids.remove(ent)
            ent = ent.split(",")
            historytripel_ids += ent
    historytripel_ids = list(set(historytripel_ids))
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
    history_latest.history_date = datetime.now()
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
