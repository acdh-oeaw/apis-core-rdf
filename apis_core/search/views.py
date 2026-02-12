from django.views.generic.edit import FormView

from apis_core.search.forms import SearchForm
from apis_core.search.models import SearchEntry


class SearchView(FormView):
    template_name = "search/search.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if query := self.request.GET.get("search", False):
            context["search_results"] = SearchEntry.objects.search(query)
        return context
