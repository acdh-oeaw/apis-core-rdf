from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from .forms import SearchForm
from .models import SearchEntry


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


class AutocompleteSuggestions(ListView):
    """
    Show `SearchEntry` autocomplete suggestions; this is meant
    to be used as autocomplete endpoint for dropdown input
    forms; the template includes a `hx-get` for every suggestion
    which points to the `AutocompleteSingleSelect` endpoint and
    swaps its content on click
    """

    template_name = "search/autocomplete_suggestions.html"
    paginate_by = 25

    def get_queryset(self):
        if q := self.request.GET.get("q"):
            content_types = self.request.GET.getlist("content_types")
            return SearchEntry.objects.search(query_str=q, content_types=content_types)
        return SearchEntry.objects.none()


class AutocompleteSingleSelect(DetailView):
    """
    Show the title of `SearchEntry` together with a hidden input
    that contains the `content_type_id` and `object_id`. This view
    is meant to be used together with `AutocompleteSuggestions` and
    be swapped on click of a suggestion
    """

    template_name = "search/autocomplete_single_select.html"
    model = SearchEntry
