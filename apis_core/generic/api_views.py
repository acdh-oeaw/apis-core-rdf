from rest_framework import viewsets
from .serializers import serializer_factory, GenericHyperlinkedModelSerializer
from .helpers import first_match_via_mro


class ModelViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for a generic model.
    The queryset is overridden by the first match from
    the `first_match_via_mro` helper.
    The serializer class is overridden by the first match from
    the `first_match_via_mro` helper.
    """

    def dispatch(self, *args, **kwargs):
        self.model = kwargs.get("contenttype").model_class()
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = first_match_via_mro(
            self.model, path="querysets", suffix="ViewSetQueryset"
        )
        return queryset or self.model.objects.all()

    def get_serializer_class(self):
        serializer_class = (
            first_match_via_mro(self.model, path="serializers", suffix="Serializer")
            or GenericHyperlinkedModelSerializer
        )
        return serializer_factory(self.model, serializer=serializer_class)
