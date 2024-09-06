from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apis_core.apis_relations.models import TempTriple
from apis_core.history.serializers import (
    HistoryLogSerializer,
    HistoryObjectSerializer,
)


class EntityHistoryLogs(ListAPIView):
    serializer_class = HistoryLogSerializer

    def get_queryset(self):
        return (
            self.kwargs.get("contenttype")
            .model_class()
            .history.filter(id=self.kwargs.get("pk"))
        )


class TempTripleHistoryLogs(ListAPIView):
    serializer_class = HistoryLogSerializer

    def get_queryset(self):
        id = self.kwargs.get("pk")
        return TempTriple.history.filter(Q(subj_id=id) | Q(obj_id=id))


class GenericHistoryLog(RetrieveAPIView):
    serializer_class = HistoryObjectSerializer

    def get_queryset(self):
        return self.kwargs.get("contenttype").model_class().objects.all()
