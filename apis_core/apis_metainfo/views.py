from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .browsingviews import GenericListView, BaseCreateView, BaseUpdateView
from .filters import UriListFilter
from .forms import UriFilterFormHelper, UriForm
from .models import Uri
from .tables import UriTable


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
    template_name = "webpage/confirm_delete.html"
    success_url = reverse_lazy("apis_core:apis_metainfo:uri_browse")
