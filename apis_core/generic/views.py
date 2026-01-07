import logging
import traceback
from collections import namedtuple
from copy import copy

from crispy_forms.layout import Field
from dal import autocomplete
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import URLValidator
from django.db import transaction
from django.db.models.fields.related import ManyToManyRel
from django.forms import modelform_factory
from django.forms.utils import pretty_name
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import select_template
from django.urls import reverse
from django.utils.text import capfirst
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django_filters.filterset import filterset_factory
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.columns import library
from django_tables2.export.views import ExportMixin
from django_tables2.tables import table_factory

from apis_core.generic.utils import get_autocomplete_data_and_normalized_uri
from apis_core.uris.models import Uri

from .filtersets import GenericFilterSet
from .forms import (
    ColumnsSelectorForm,
    GenericEnrichForm,
    GenericImportForm,
    GenericMergeWithForm,
    GenericModelForm,
    GenericSelectMergeOrEnrichForm,
)
from .helpers import (
    first_member_match,
    generate_search_filter,
    module_paths,
    permission_fullname,
    template_names_via_mro,
)
from .tables import GenericTable

logger = logging.getLogger(__name__)


class Overview(TemplateView):
    template_name = "generic/overview.html"


class GenericModelPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Verify that the current user has the required permission for this model.
    The model overrides the `PermissionRequiredMixin.get_permission_required`
    method to generate the required permission name on the fly, based on a
    verb (`permission_action_required`) and the model this view act upon.
    This allows us to set `permission_action_required` simply to `add`, or
    `view` and reuse the mixin for views that work with different models.
    In addition, for the views that have `permission_action_required` set to
    `view`, it check if there is the global setting `APIS_ANON_VIEWS_ALLOWED`
    set to `True`, which permits anonymouse users access to the view.
    """

    def get_permission_required(self):
        if not hasattr(self, "model"):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the model attribute"
            )
        if getattr(self, "permission_action_required", None) == "view" and getattr(
            settings, "APIS_ANON_VIEWS_ALLOWED", False
        ):
            return []
        if hasattr(self, "permission_action_required"):
            return [permission_fullname(self.permission_action_required, self.model)]
        return []


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
            # Some parent classes come with custom template_names,
            # some need a `.template_name` attribute set. For the
            # latter ones we handle the missing `.template_name`
            # gracefully
            try:
                template_names = super().get_template_names()
            except ImproperlyConfigured:
                pass
        suffix = ".html"
        if hasattr(self, "template_name_suffix"):
            suffix = self.template_name_suffix + ".html"
        additional_templates = template_names_via_mro(self.model, suffix=suffix)
        template_names += filter(
            lambda template: template not in template_names, additional_templates
        )
        return template_names


class List(
    GenericModelMixin,
    GenericModelPermissionRequiredMixin,
    ExportMixin,
    SingleTableMixin,
    FilterView,
):
    """
    List view for a generic model.
    Access requires the `<model>_view` permission.
    It is based on django-filters FilterView and django-tables SingleTableMixin.
    The table class is overridden by the first match from
    the `first_member_match` helper.
    The filterset class is overridden by the first match from
    the `first_member_match` helper.
    The queryset is overridden by the first match from
    the `first_member_match` helper.
    """

    template_name_suffix = "_list"
    permission_action_required = "view"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self.model)
        self.cookie_name = f"{content_type.app_label}.{content_type.model}"
        self.params = self.request.GET.copy()

    def _get_prefix_params(self, prefix: str):
        """
        Get the request parameters with a specific prefix.
        If there are no request parameters with that prefix,
        fall back to the cookie for that prefix.
        """
        params = self.params.copy()
        for key in self.params:
            if not key.startswith(prefix):
                del params[key]
        cookie_name = f"{self.cookie_name}_{prefix}"
        return params or QueryDict(self.request.COOKIES.get(cookie_name, ""))

    def _remember_fields(self, prefix: str) -> bool:
        remember_field_name = f"{prefix}-remember"
        params = self._get_prefix_params(prefix)
        return params.get(remember_field_name, "off") == "on"

    def _set_form_cookie(self, response, prefix: str):
        """
        Update the cookie with the current request params.
        Unless the `remember` parameter was sent for the given
        prefix, tell the client to delete the cookie.
        """
        cookie_name = f"{self.cookie_name}_{prefix}"
        params = self._get_prefix_params(prefix)
        if params:
            response.set_cookie(cookie_name, params.urlencode())

        if not self._remember_fields(prefix):
            response.delete_cookie(cookie_name)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        self._set_form_cookie(response, "filterset")
        self._set_form_cookie(response, "choices")

        return response

    def get_table_class(self):
        table_modules = module_paths(self.model, path="tables", suffix="Table")
        table_class = first_member_match(table_modules, GenericTable)
        return table_factory(self.model, table_class)

    export_formats = getattr(settings, "EXPORT_FORMATS", ["csv", "json"])

    def get_export_filename(self, extension):
        table_class = self.get_table_class()
        if hasattr(table_class, "export_filename"):
            return f"{table_class.export_filename}.{extension}"

        return super().get_export_filename(extension)

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()

        selected_columns = self._get_prefix_params("choices").getlist(
            "choices-columns", []
        )
        modelfields = self.model._meta.get_fields()
        # if the form was submitted, we look at the selected
        # columns and exclude all columns that are not part of that list
        if self.params and selected_columns:
            columns_exclude = self.get_filterset_class().Meta.form.columns_exclude
            other_columns = [
                name for (name, field) in self._get_columns_choices(columns_exclude)
            ]
            kwargs["exclude"] = [
                field for field in other_columns if field not in selected_columns
            ]

        # now we look at the selected columns and
        # add all modelfields and annotated fields that
        # are part of the selected columns to the extra_columns
        annotationfields = list()
        for key, value in self.object_list.query.annotations.items():
            # we have to use copy, so we don't edit the original field
            fake_field = copy(getattr(value, "field", value.output_field))
            setattr(fake_field, "name", key)
            annotationfields.append(fake_field)
        extra_fields = list(
            filter(
                lambda x: x.name in selected_columns,
                modelfields + tuple(annotationfields),
            )
        )
        kwargs["extra_columns"] = [
            (field.name, library.column_for_field(field, accessor=field.name))
            for field in extra_fields
            if field.name not in self.get_table_class().base_columns
        ]

        return kwargs

    def get_filterset_class(self):
        filterset_modules = module_paths(
            self.model, path="filtersets", suffix="FilterSet"
        )
        filterset_class = first_member_match(filterset_modules, GenericFilterSet)
        return filterset_factory(self.model, filterset_class)

    def _get_columns_choices(self, columns_exclude):
        # lets start with the custom table fields
        choices = {
            key.name: capfirst(str(key) or key.name or "Nameless column")
            for key in self.get_table().columns
        }
        # then add the model fields, but only the ones
        # that are not automatically created (parent keys)
        # and not the m2m relations and not any that are
        # already part of the choices
        choices |= {
            field.name: pretty_name(getattr(field, "verbose_name", field.name))
            for field in self.model._meta.get_fields()
            if not getattr(field, "auto_created", False)
            and not isinstance(field, ManyToManyRel)
            and field.name not in choices.keys()
        }
        # finally we add any annotated fields
        choices |= {key: key for key in self.get_queryset().query.annotations.keys()}
        # now we drop all the choices that are listed in columns_exclude
        choices = {
            key: value for key, value in choices.items() if key not in columns_exclude
        }
        return choices.items()

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["prefix"] = "filterset"
        kwargs["data"] = self._get_prefix_params("filterset")
        return kwargs

    def get_filterset(self, filterset_class):
        """
        We override the `get_filterset` method, so we can add a
        css class to the the selected filters
        """
        filterset = super().get_filterset(filterset_class)

        # If the filterset form contains form data
        # we add a CSS class to the element wrapping
        # that field in HTML. This CSS class can be
        # used to emphasize the fields that are used.
        # To be able to compare the fields with the form
        # data, we create a temporary mapping between
        # widget_names and fields
        fields = {}
        for name, field in filterset.form.fields.items():
            fields[name] = name
            if hasattr(field.widget, "widgets_names"):
                for widget_name in field.widget.widgets_names:
                    fields[name + widget_name] = name
        if filterset.form.is_valid():
            data = filterset.form.cleaned_data
            for param in [param for param, value in data.items() if value]:
                if fieldname := fields.get(param, None):
                    filterset.form.helper[fieldname].wrap(
                        Field, wrapper_class="filter-input-selected"
                    )

        return filterset

    def get_queryset(self):
        queryset_methods = module_paths(
            self.model, path="querysets", suffix="ListViewQueryset"
        )
        queryset = first_member_match(queryset_methods) or (lambda x: x)
        return queryset(self.model.objects.all())

    def get_table_pagination(self, table):
        """
        Override `get_table_pagination` from the tables2 TableMixinBase,
        so we can set the table_pagination value as attribute of the table.
        """
        self.table_pagination = getattr(table, "table_pagination", None)
        return super().get_table_pagination(table)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        table = context.get("table", None)
        filterset = context.get("filter", None)
        context["filterset_remember"] = self._remember_fields("filterset")
        if table and filterset:
            columns_exclude = filterset.form.columns_exclude
            initial_columns = [
                col.name for col in table.columns if col.name not in columns_exclude
            ]
            if choices := self._get_columns_choices(columns_exclude=columns_exclude):
                context["columns_selector"] = ColumnsSelectorForm(
                    choices=choices,
                    initial={"choices": initial_columns},
                    prefix="choices",
                    data=self._get_prefix_params("choices") or None,
                )
        return context


class Detail(GenericModelMixin, GenericModelPermissionRequiredMixin, DetailView):
    """
    Detail view for a generic model.
    Access requires the `<model>_view` permission.
    """

    permission_action_required = "view"


class Create(
    GenericModelMixin,
    GenericModelPermissionRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """
    Create view for a generic model.
    Access requires the `<model>_add` permission.
    The form class is overridden by the first match from
    the `first_member_match` helper.
    """

    template_name_suffix = "_create"
    permission_action_required = "add"

    def get_form_class(self):
        form_modules = module_paths(self.model, path="forms", suffix="Form")
        form_class = first_member_match(form_modules, GenericModelForm)
        return modelform_factory(self.model, form_class)

    def get_success_message(self, cleaned_data):
        message_templates = template_names_via_mro(
            self.model, suffix="_create_success_message.html"
        )
        template = select_template(message_templates)
        return template.render({"object": self.object})

    def get_success_url(self):
        return self.object.get_create_success_url()


class Delete(GenericModelMixin, GenericModelPermissionRequiredMixin, DeleteView):
    """
    Delete view for a generic model.
    Access requires the `<model>_delete` permission.
    """

    permission_action_required = "delete"

    def get_success_url(self):
        if redirect := self.request.GET.get("redirect"):
            return redirect
        return reverse(
            "apis_core:generic:list",
            args=[self.request.resolver_match.kwargs["contenttype"]],
        )


class Update(
    GenericModelMixin,
    GenericModelPermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """
    Update view for a generic model.
    Access requires the `<model>_change` permission.
    The form class is overridden by the first match from
    the `first_member_match` helper.
    """

    permission_action_required = "change"

    def get_form_class(self):
        form_modules = module_paths(self.model, path="forms", suffix="Form")
        form_class = first_member_match(form_modules, GenericModelForm)
        return modelform_factory(self.model, form_class)

    def get_success_message(self, cleaned_data):
        message_templates = template_names_via_mro(
            self.model, suffix="_update_success_message.html"
        )
        template = select_template(message_templates)
        return template.render({"object": self.object})

    def get_success_url(self):
        return self.object.get_update_success_url()


class Duplicate(GenericModelMixin, GenericModelPermissionRequiredMixin, View):
    permission_action_required = "add"

    def get(self, request, *args, **kwargs):
        source_obj = get_object_or_404(self.model, pk=kwargs["pk"])
        newobj = source_obj.duplicate()

        message_templates = template_names_via_mro(
            self.model, suffix="_duplicate_success_message.html"
        )
        template = select_template(message_templates)
        messages.success(request, template.render({"object": source_obj}))
        return redirect(newobj.get_edit_url())


class Autocomplete(
    GenericModelMixin,
    GenericModelPermissionRequiredMixin,
    autocomplete.Select2QuerySetView,
):
    """
    Autocomplete view for a generic model.
    Access requires the `<model>_view` permission.
    The queryset is overridden by the first match from
    the `first_member_match` helper.
    """

    permission_action_required = "view"
    template_name_suffix = "_autocomplete_result"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        # We use a URI parameter to enable the create functionality in the
        # autocomplete dropdown. It is not important what the value of the
        # `create_field` is, because we override create_object anyway.
        self.create_field = self.request.GET.get("create", None)
        try:
            template = select_template(self.get_template_names())
            self.template = template.template.name
        except TemplateDoesNotExist:
            self.template = None

    def get_queryset(self):
        queryset_methods = module_paths(
            self.model, path="querysets", suffix="AutocompleteQueryset"
        )
        queryset = first_member_match(queryset_methods)
        if queryset:
            return queryset(self.model, self.q)
        return self.model.objects.filter(generate_search_filter(self.model, self.q))

    def get_results(self, context):
        external_only = self.kwargs.get("external_only", False)
        results = [] if external_only else super().get_results(context)
        queryset_methods = module_paths(
            self.model, path="querysets", suffix="ExternalAutocomplete"
        )
        ExternalAutocomplete = first_member_match(queryset_methods)
        if ExternalAutocomplete:
            results.extend(ExternalAutocomplete().get_results(self.q))
        return results

    def create_object(self, value):
        """
        We try multiple approaches to create a model instance from a value:
        * we first test if the value is an URL and if so we expect it to be
        something that can be imported using one of the configured importers
        and so we pass the value to the import logic.
        * if the value is not a string, we try to pass it to the `create_from_string`
        method of the model, if that does exist. Its the models responsibility to
        implement this method and the method should somehow know how to create
        model instance from the value...
        * finally we pass the value to the `create_object` method from the DAL
        view, which tries to pass it to `get_or_create` which likely also fails,
        but this is expected and we raise a more useful exception.
        """
        try:
            URLValidator()(value)
            return self.queryset.model.import_from(value)
        except ValidationError:
            pass
        try:
            return self.queryset.model.create_from_string(value)
        except AttributeError:
            raise ImproperlyConfigured(
                f'Model "{self.queryset.model._meta.verbose_name}" not configured to create from string'
            )

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().post(request, *args, **kwargs)
        except Exception as e:
            logger.debug(traceback.format_exc())
            return http.JsonResponse({"error": str(e)})


class Import(GenericModelMixin, GenericModelPermissionRequiredMixin, FormView):
    template_name_suffix = "_import"
    permission_action_required = "add"

    def get_form_class(self):
        form_modules = module_paths(self.model, path="forms", suffix="ImportForm")
        form_class = first_member_match(form_modules, GenericImportForm)
        return modelform_factory(self.model, form_class)

    def form_valid(self, form):
        self.object = form.cleaned_data["url"]
        for field, error in getattr(self.object, "_import_errors", {}).items():
            messages.error(self.request, f"Could not set {field}: {error}")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class SelectMergeOrEnrich(
    GenericModelMixin, GenericModelPermissionRequiredMixin, FormView
):
    """
    This view provides a simple form that allows to select other entities (also from
    external sources, if set up) and on form submit redirects to the Enrich view.
    """

    template_name_suffix = "_selectmergeorenrich"
    permission_action_required = "add"
    form_class = GenericSelectMergeOrEnrichForm

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, pk=self.kwargs.get("pk"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["object"] = self.get_object()
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["content_type"] = ContentType.objects.get_for_model(self.model)
        return kwargs

    def form_valid(self, form):
        uri = form.cleaned_data["uri"]
        if uri.isdigit():
            return redirect(self.get_object().get_merge_url(uri))
        return redirect(self.get_object().get_enrich_url() + f"?uri={uri}")


class MergeWith(GenericModelMixin, GenericModelPermissionRequiredMixin, FormView):
    """
    Generic merge view.
    """

    permission_action_required = "change"
    form_class = GenericMergeWithForm
    template_name_suffix = "_merge"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.object = get_object_or_404(self.model, pk=self.kwargs["pk"])
        self.other = get_object_or_404(self.model, pk=self.kwargs["otherpk"])

    def get_context_data(self, **kwargs):
        """
        The context consists of the two objects that are merged as well
        as a list of changes. Those changes are presented in the view as
        a table with diffs
        """
        Change = namedtuple("Change", "field old new")
        ctx = super().get_context_data(**kwargs)
        ctx["changes"] = []
        for field in self.object._meta.fields:
            newval = self.object.get_field_value_after_merge(self.other, field)
            ctx["changes"].append(
                Change(field.verbose_name, getattr(self.object, field.name), newval)
            )
        ctx["object"] = self.object
        ctx["other"] = self.other
        return ctx

    def form_valid(self, form):
        self.object.merge_with([self.other])
        messages.info(self.request, f"Merged values of {self.other} into {self.object}")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class Enrich(GenericModelMixin, GenericModelPermissionRequiredMixin, FormView):
    """
    Enrich an entity with data from an external source
    Provides the user with a form to select the fields that should be updated.
    """

    permission_action_required = "change"
    template_name_suffix = "_enrich"
    form_class = GenericEnrichForm
    importer_class = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.object = get_object_or_404(self.model, pk=self.kwargs["pk"])
        _, self.uri = get_autocomplete_data_and_normalized_uri(
            self.request.GET.get("uri")
        )
        if not self.uri:
            messages.error(self.request, "No uri parameter specified.")

    def get(self, *args, **kwargs):
        try:
            uriobj = Uri.objects.get(uri=self.uri)
            if uriobj.object_id != self.object.id:
                messages.info(
                    self.request,
                    f"Object with URI {self.uri} already exists, you were redirected to the merge form.",
                )
                return redirect(self.object.get_merge_url(uriobj.object_id))
        except Uri.DoesNotExist:
            pass
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object"] = self.object
        ctx["uri"] = self.uri
        return ctx

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["instance"] = self.object
        try:
            self.data = self.model.fetch_from(self.request.GET.get("uri"))
            kwargs["data"] = self.data
        except ImproperlyConfigured as e:
            messages.error(self.request, e)
        return kwargs

    def form_valid(self, form):
        """
        Go through all the form fields and extract the ones that
        start with `update_` and that are set (those are the checkboxes that
        select which fields to update).
        Create a dict from those values, add the uri and pass the dict on to
        the models `import_data` method.
        """
        data = {}
        for key, values in self.request.POST.items():
            if key.startswith("update_"):
                key = key.removeprefix("update_")
                data[key] = self.data[key]
        data["same_as"] = [self.uri] + data.get("same_as", [])
        if data:
            self.object.import_data(data)
            for field, error in getattr(self.object, "_import_errors", {}).items():
                messages.error(self.request, f"Could not update {field}: {error}")
        messages.info(self.request, f"Updated fields {data.keys()}")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
