from django_filters.rest_framework import DjangoFilterBackend
from .filtersets import filterset_factory, GenericFilterSet
from .helpers import module_paths, first_member_match


class GenericFilterBackend(DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        filterset_api_class_modules = module_paths(
            view.model, path="filtersets", suffix="ApiFilterSet"
        )
        filterset_class_modules = module_paths(
            view.model, path="filtersets", suffix="FilterSet"
        )
        filterset_class = first_member_match(
            filterset_api_class_modules + filterset_class_modules, GenericFilterSet
        )
        return filterset_factory(view.model, filterset_class)
