from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from .browsingviews import GenericListView, BaseCreateView, BaseUpdateView
from .filters import UriListFilter
from .forms import UriFilterFormHelper, UriForm, UriGetOrCreateForm
from .models import Uri
from .tables import UriTable
from apis_core.utils.rdf import get_modelname_and_dict_from_uri
from apis_core.utils.normalize import clean_uri


class UriListView(GenericListView):
    model = Uri
    filter_class = UriListFilter
    formhelper_class = UriFilterFormHelper
    table_class = UriTable
    init_columns = [
        "id",
        "uri",
        "entity",
    ]
    enable_merge = True


class UriDetailView(DetailView):
    model = Uri
    template_name = "apis_metainfo/uri_detail.html"


class UriCreate(LoginRequiredMixin, BaseCreateView):
    model = Uri
    form_class = UriForm


class UriUpdate(LoginRequiredMixin, BaseUpdateView):
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
