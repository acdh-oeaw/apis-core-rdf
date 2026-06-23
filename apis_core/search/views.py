from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from apis_core.search.forms import SearchForm
from apis_core.search.models import SearchEntry


class SearchView(ListView, FormMixin):
    template_name = "search/search.html"
    form_class = SearchForm
    paginate_by = 25

    def get_queryset(self):
        form = self.get_form_class()(self.request.GET)
        if form.is_valid():
            return SearchEntry.objects.search(**form.cleaned_data)
        return SearchEntry.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET:
            kwargs["data"] = self.request.GET
        return kwargs
