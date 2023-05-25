from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry

from .browsingviews import GenericListView, BaseCreateView, BaseUpdateView
from .filters import UriListFilter
from .forms import UriFilterFormHelper, UriForm, UriGetOrCreateForm
from .models import Uri
from .tables import UriTable
from apis_core.utils.rdf import get_modelname_and_dict_from_uri
from apis_core.utils.normalize import clean_uri

from apis_core.apis_entities.models import TempEntityClass

from datetime import datetime, timedelta, timezone


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


class Index(LoginRequiredMixin, TemplateView):
    template_name = "apis_metainfo/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_entities"] = dict()
        cts = ContentType.objects.all()
        cts = [ct for ct in cts if ct.model_class()]
        for ct in cts:
            if issubclass(ct.model_class(), TempEntityClass) and ct.model_class() != TempEntityClass:
                if ct.app_label not in context["all_entities"]:
                    context["all_entities"][ct.app_label] = dict()
                context["all_entities"][ct.app_label][ct.name] = ct.model_class().objects.count()
        two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)
        les = LogEntry.objects.filter(action_time__gte=two_weeks_ago)
        context["logentries"] = les
        return context
