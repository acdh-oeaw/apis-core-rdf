from rest_framework import viewsets
from .serializers import serializer_factory, GenericHyperlinkedModelSerializer
from .helpers import module_paths, first_member_match


class ModelViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for a generic model.
    The queryset is overridden by the first match from
    the `first_member_match` helper.
    The serializer class is overridden by the first match from
    the `first_member_match` helper.
    """

    def dispatch(self, *args, **kwargs):
        self.model = kwargs.get("contenttype").model_class()
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset_methods = module_paths(
            self.model, path="querysets", suffix="ViewSetQueryset"
        )
        queryset = first_member_match(queryset_methods) or (lambda x: x)
        return queryset(self.model.objects.all())

    def get_serializer_class(self):
        renderer = self.request.accepted_renderer
        serializer_class_modules = module_paths(
            self.model, path="serializers", suffix="Serializer"
        )
        serializer_class = first_member_match(
            serializer_class_modules,
            getattr(renderer, "serializer", GenericHyperlinkedModelSerializer),
        )
        return serializer_factory(self.model, serializer=serializer_class)
