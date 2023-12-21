from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import get_permission_codename
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.forms import modelform_factory

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.tables import table_factory
from django_tables2.columns import library
from dal import autocomplete

from .tables import GenericTable
from .filtersets import filterset_factory, GenericFilterSet
from .forms import GenericModelForm
from .helpers import first_match_via_mro, template_names_via_mro, generate_search_filter


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
        self.model = kwargs.get("contenttype").model_class()
        self.queryset = self.model.objects.all()

    def get_template_names(self):
        template_names = super().get_template_names()
        suffix = self.template_name_suffix + ".html"
        additional_templates = template_names_via_mro(self.model, suffix) + [
            f"generic/generic{suffix}"
        ]
        template_names += filter(
            lambda template: template not in template_names, additional_templates
        )
        return template_names

    def get_permission_required(self):
        if hasattr(self, "permission_action_required"):
            return [
                get_permission_codename(
                    self.permission_action_required, self.model._meta
                )
            ]
        return []


class List(GenericModelMixin, PermissionRequiredMixin, SingleTableMixin, FilterView):
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
        return (
            first_match_via_mro(self.model, path="querysets", suffix="ListViewQueryset")
            or self.model.objects.all()
        )


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
        return reverse(
            "apis:generic:list",
            args=[self.request.resolver_match.kwargs["contenttype"]],
        )


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
        return reverse(
            "apis:generic:list",
            args=[self.request.resolver_match.kwargs["contenttype"]],
        )


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

    def get_queryset(self):
        queryset = first_match_via_mro(
            self.model, path="querysets", suffix="AutocompleteQueryset"
        )
        if queryset:
            return queryset(self.model, self.q)
        return self.model.objects.filter(generate_search_filter(self.model, self.q))