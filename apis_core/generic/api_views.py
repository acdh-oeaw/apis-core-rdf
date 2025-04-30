from rest_framework import viewsets

from apis_core.generic.schema import GenericAutoSchema

from .filterbackends import GenericFilterBackend
from .helpers import first_member_match, makeclassprefix, module_paths
from .serializers import GenericHyperlinkedModelSerializer, serializer_factory


class ModelViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for a generic model.
    The queryset is overridden by the first match from
    the `first_member_match` helper.
    The serializer class is overridden by the first match from
    the `first_member_match` helper.
    """

    filter_backends = [GenericFilterBackend]
    schema = GenericAutoSchema()

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
        renderer = getattr(getattr(self, "request", {}), "accepted_renderer", None)
        serializer_class_modules = module_paths(
            self.model, path="serializers", suffix="Serializer"
        )
        if renderer is not None:
            prefix = makeclassprefix(renderer.format)
            serializer_class_modules = (
                module_paths(
                    self.model, path="serializers", suffix=f"{prefix}Serializer"
                )
                + serializer_class_modules
            )

        serializer_class = first_member_match(
            serializer_class_modules,
            getattr(renderer, "serializer", GenericHyperlinkedModelSerializer),
        )
        return serializer_factory(
            self.model, serializer=serializer_class, action=self.action
        )
