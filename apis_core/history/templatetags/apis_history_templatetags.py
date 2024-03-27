from datetime import datetime
from apis_core.history.serializers import HistoryLogSerializer
from apis_core.history.views import convert_timestamps
from django import template
from apis_core.history.utils import triple_sidebar_history

register = template.Library()


@register.simple_tag(takes_context=True)
def object_relations_history(context, detail=True):
    obj = context["object"]
    return triple_sidebar_history(
        obj.pk, obj.__class__.__name__.lower(), context["request"], detail
    )


@register.filter
def get_history_data(obj):
    data = HistoryLogSerializer(obj.get_history_data(), many=True).data
    data = sorted(
        [convert_timestamps(x) for x in data],
        key=lambda x: datetime.strptime(x["timestamp"], "%d.%m.%Y %H:%M"),
        reverse=True,
    )
    return data
