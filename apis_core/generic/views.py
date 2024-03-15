from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from django.forms import modelform_factory
from django.template.loader import select_template
from django.template.exceptions import TemplateDoesNotExist

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.tables import table_factory
from django_tables2.columns import library
from dal import autocomplete

from .tables import GenericTable
from .filtersets import filterset_factory, GenericFilterSet
from .forms import GenericModelForm, GenericImportForm
from .helpers import (
    first_match_via_mro,
    template_names_via_mro,
    generate_search_filter,
    permission_fullname,
)
from apis_core.utils.helpers import create_object_from_uri

from apis_core.core.mixins import ListViewObjectFilterMixin


class Overview(TemplateView):
    template_name = "generic/overview.html"


class GenericModelMixin:
    """
    A mixin providing the common functionality for all the views working
    with `generic` models - that is models that are accessed via the
    contenttype framework (using `app_label.model`).
    It sets the `.model` of the view and generates a list of possible template
    names (based on the MRO of the model).
    If the view has a `permission_action_required` attribute, this is used
    to set the permission required to access the view for this specific model.
    """

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if contenttype := kwargs.get("contenttype"):
            self.model = contenttype.model_class()
            self.queryset = self.model.objects.all()

    def get_template_names(self):
        template_names = []
        if hasattr(super(), "get_template_names"):
            template_names = super().get_template_names()
        suffix = ".html"
        if hasattr(self, "template_name_suffix"):
            suffix = self.template_name_suffix + ".html"
        additional_templates = template_names_via_mro(self.model, suffix) + [
            f"generic/generic{suffix}"
        ]
        template_names += filter(
            lambda template: template not in template_names, additional_templates
        )
        return template_names

    def get_permission_required(self):
        if hasattr(settings, "APIS_VIEW_PASSES_TEST"):
            if settings.APIS_VIEW_PASSES_TEST(self):
                return []
        if hasattr(self, "permission_action_required"):
            return [permission_fullname(self.permission_action_required, self.model)]
        return []


class List(
    ListViewObjectFilterMixin,
    GenericModelMixin,
    PermissionRequiredMixin,
    SingleTableMixin,
    FilterView,
):
    """
    List view for a generic model.
    Access requires the `<model>_view` permission.
    It is based on django-filters FilterView and django-tables SingleTableMixin.
    The table class is overridden by the first match from
    the `first_match_via_mro` helper.
    The filterset class is overridden by the first match from
    the `first_match_via_mro` helper.
    The queryset is overridden by the first match from
    the `first_match_via_mro` helper.
    """

    template_name_suffix = "_list"
    permission_action_required = "view"

    def get_table_class(self):
        table_class = (
            first_match_via_mro(self.model, path="tables", suffix="Table")
            or GenericTable
        )
        return table_factory(self.model, table_class)

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        columns = self.request.GET.getlist("columns", [])
        column_fields = [
            field for field in self.model._meta.fields if field.name in columns
        ]
        kwargs["extra_columns"] = [
            (field.name, library.column_for_field(field, accessor=field.name))
            for field in column_fields
        ]
        return kwargs

    def get_filterset_class(self):
        filterset_class = (
            first_match_via_mro(self.model, path="filtersets", suffix="FilterSet")
            or GenericFilterSet
        )
        return filterset_factory(self.model, filterset_class)

    def get_queryset(self):
        queryset = first_match_via_mro(
            self.model, path="querysets", suffix="ListViewQueryset"
        ) or (lambda x: x)
        return self.filter_queryset(queryset(self.model.objects.all()))


class Detail(GenericModelMixin, PermissionRequiredMixin, DetailView):
    """
    Detail view for a generic model.
    Access requires the `<model>_view` permission.
    """

    permission_action_required = "view"


class Create(GenericModelMixin, PermissionRequiredMixin, CreateView):
    """
    Create view for a generic model.
    Access requires the `<model>_add` permission.
    The form class is overridden by the first match from
    the `first_match_via_mro` helper.
    """

    template_name = "generic/generic_form.html"
    permission_action_required = "add"

    def get_form_class(self):
        form_class = (
            first_match_via_mro(self.model, path="forms", suffix="Form")
            or GenericModelForm
        )
        return modelform_factory(self.model, form_class)

    def get_success_url(self):
        return self.object.get_edit_url()


class Delete(GenericModelMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete view for a generic model.
    Access requires the `<model>_delete` permission.
    """

    permission_action_required = "delete"

    def get_success_url(self):
        return reverse(
            "apis:generic:list",
            args=[self.request.resolver_match.kwargs["contenttype"]],
        )

    def delete(self, *args, **kwargs):
        if "HX-Request" in self.request.headers:
            return (
                reverse_lazy(
                    "apis:generic:list",
                    args=[self.request.resolver_match.kwargs["contenttype"]],
                ),
            )
        return super().delete(*args, **kwargs)


class Update(GenericModelMixin, PermissionRequiredMixin, UpdateView):
    """
    Update view for a generic model.
    Access requires the `<model>_change` permission.
    The form class is overridden by the first match from
    the `first_match_via_mro` helper.
    """

    permission_action_required = "change"

    def get_form_class(self):
        form_class = (
            first_match_via_mro(self.model, path="forms", suffix="Form")
            or GenericModelForm
        )
        return modelform_factory(self.model, form_class)

    def get_success_url(self):
        return self.object.get_edit_url()


class Autocomplete(
    GenericModelMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView
):
    """
    Autocomplete view for a generic model.
    Access requires the `<model>_view` permission.
    The queryset is overridden by the first match from
    the `first_match_via_mro` helper.
    """

    permission_action_required = "view"
    template_name_suffix = "_autocomplete_result"
    create_field = "thisisnotimportant"  # because we are using create_object_from_uri

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        try:
            template = select_template(self.get_template_names())
            self.template = template.template.name
        except TemplateDoesNotExist:
            self.template = None

    def get_queryset(self):
        queryset = first_match_via_mro(
            self.model, path="querysets", suffix="AutocompleteQueryset"
        )
        if queryset:
            return queryset(self.model, self.q)
        return self.model.objects.filter(generate_search_filter(self.model, self.q))

    def get_results(self, context):
        external_only = self.kwargs.get("external_only", False)
        results = [] if external_only else super().get_results(context)
        ExternalAutocomplete = first_match_via_mro(
            self.model, path="querysets", suffix="ExternalAutocomplete"
        )
        if ExternalAutocomplete:
            results.extend(ExternalAutocomplete().get_results(self.q))
        return results

    def create_object(self, value):
        return create_object_from_uri(value, self.queryset.model)


class Import(GenericModelMixin, PermissionRequiredMixin, FormView):
    template_name = "generic/generic_import_form.html"
    template_name_suffix = "_import"
    permission_action_required = "create"

    def get_form_class(self):
        form_class = (
            first_match_via_mro(self.model, path="forms", suffix="ImportForm")
            or GenericImportForm
        )
        return modelform_factory(self.model, form_class)

    def form_valid(self, form):
        self.object = form.cleaned_data["url"]
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
