from rest_framework.generics import ListAPIView, RetrieveAPIView

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


class GenericHistoryLog(RetrieveAPIView):
    serializer_class = HistoryObjectSerializer

    def get_queryset(self):
        return self.kwargs.get("contenttype").model_class().objects.all()
