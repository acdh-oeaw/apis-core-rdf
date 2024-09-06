from django.db.models import Q
from django.template import loader
from rest_framework.filters import SearchFilter

from apis_core.apis_entities.utils import get_entity_classes
from apis_core.generic.helpers import generate_search_filter


class CustomSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset
        entities = get_entity_classes()
        q = Q()
        for entity in entities:
            name = entity._meta.model_name
            q |= Q(**{f"{name}__isnull": False}) & generate_search_filter(
                entity, search_terms, prefix=f"{name}__"
            )
        return queryset.filter(q)

    def to_html(self, request, queryset, view):
        context = {
            "param": self.search_param,
            "term": request.query_params.get(self.search_param, ""),
        }
        template = loader.get_template(self.template)
        return template.render(context)
