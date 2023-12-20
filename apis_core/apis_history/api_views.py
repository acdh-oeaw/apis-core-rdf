from django.http import Http404
from rest_framework import routers
from rest_framework.viewsets import ReadOnlyModelViewSet
from apis_core.apis_history.serializers import HistoryLogSerializer
from django.contrib.contenttypes.models import ContentType
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins


class GenericHistoryLogs(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = HistoryLogSerializer

    def get_queryset(self):
        id = self.request.query_params.get("id", None)
        model = self.request.query_params.get("entity_type", None)
        if id is None:
            raise Http404("No id provided")
        if model is None:
            raise Http404("No model provided")
        cls = ContentType.objects.get(app_label="apis_ontology", model=model)
        exclude = []
        qs = cls.model_class().history.filter(id=id)
        for q in qs:
            id1 = q.history_id
            ts = q.history_date
            exclude.extend(
                cls.model_class()
                .history.filter(history_id__lt=id1, history_date=ts)
                .values_list("history_id", flat=True)
            )
        return qs.exclude(history_id__in=exclude)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("entity_type", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
