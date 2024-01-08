from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from .filters import UriListFilter
from .forms import UriFilterFormHelper, UriForm, UriGetOrCreateForm
from .models import Uri
from .tables import UriTable


class UriListView(SingleTableMixin, FilterView):
    model = Uri
    filterset_class = UriListFilter
    formhelper_class = UriFilterFormHelper
    table_class = UriTable
    template_name = getattr(settings, "APIS_LIST_VIEW_TEMPLATE", "generic_list.html")

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)
        filterset = filterset_class(**kwargs)
        filterset.form.helper = self.formhelper_class()
        return filterset


class UriDetailView(DetailView):
    model = Uri
    template_name = "apis_metainfo/uri_detail.html"


class UriCreate(LoginRequiredMixin, CreateView):
    model = Uri
    form_class = UriForm


class UriUpdate(LoginRequiredMixin, UpdateView):
    model = Uri
    form_class = UriForm


class UriDelete(LoginRequiredMixin, DeleteView):
    model = Uri
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("apis_core:apis_metainfo:uri_browse")


class UriGetOrCreate(FormView):
    template_name = "uri_create.html"
    form_class = UriGetOrCreateForm

    def form_valid(self, form):
        if form.is_valid():
            self.success_url = form.uriobj.root_object.get_absolute_url()
        return super().form_valid(form)
