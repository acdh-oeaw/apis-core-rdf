from django_filters.filterset import filterset_factory
from django_filters.rest_framework import DjangoFilterBackend

from .filtersets import GenericFilterSet
from .helpers import first_member_match, module_paths


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
