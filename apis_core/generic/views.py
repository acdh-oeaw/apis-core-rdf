from collections import namedtuple
from copy import copy

from dal import autocomplete
from django import forms, http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import URLValidator
from django.db.models.fields.related import ManyToManyRel
from django.forms import modelform_factory
from django.forms.utils import pretty_name
from django.shortcuts import get_object_or_404, redirect
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import select_template
from django.urls import reverse
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

from apis_core.apis_metainfo.models import Uri
from apis_core.apis_metainfo.utils import create_object_from_uri
from apis_core.utils.helpers import get_importer_for_model

from .filtersets import GenericFilterSet
from .forms import (
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
        additional_templates = template_names_via_mro(self.model, suffix) + [
            f"generic/generic{suffix}"
        ]
        template_names += filter(
            lambda template: template not in template_names, additional_templates
        )
        return template_names

    def get_permission_required(self):
        if getattr(self, "permission_action_required", None) == "view" and getattr(
            settings, "APIS_ANON_VIEWS_ALLOWED", False
        ):
            return []
        if hasattr(self, "permission_action_required"):
            return [permission_fullname(self.permission_action_required, self.model)]
        return []


class List(
    GenericModelMixin,
    PermissionRequiredMixin,
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

        # we look at the selected columns and exclude
        # all modelfields that are not part of that list
        form = self.get_filterset(self.get_filterset_class()).form
        initial = form.fields["columns"].initial if "columns" in form.fields else []
        selected_columns = self.request.GET.getlist("columns", initial)
        modelfields = self.model._meta.get_fields()
        kwargs["exclude"] = [
            field.name for field in modelfields if field.name not in selected_columns
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
        # we start with the model fields
        choices = [
            (field.name, pretty_name(getattr(field, "verbose_name", field.name)))
            for field in self.model._meta.get_fields()
            if not getattr(field, "auto_created", False)
            and not isinstance(field, ManyToManyRel)
        ]
        # we add any annotated fields to that
        choices += [(key, key) for key in self.get_queryset().query.annotations.keys()]
        # now we drop all the choices that are listed in columns_exclude
        choices = list(filter(lambda x: x[0] not in columns_exclude, choices))
        return choices

    def _get_columns_initial(self, columns_exclude):
        return [
            field
            for field in self.get_table().columns.names()
            if field not in columns_exclude
        ]

    def get_filterset(self, filterset_class):
        """
        We override the `get_filterset` method, so we can inject a
        `columns` selector into the form
        """
        filterset = super().get_filterset(filterset_class)
        columns_exclude = filterset.form.columns_exclude

        # we inject a `columns` selector in the beginning of the form
        if choices := self._get_columns_choices(columns_exclude):
            columns = forms.MultipleChoiceField(
                required=False,
                choices=choices,
                initial=self._get_columns_initial(columns_exclude),
            )
            filterset.form.fields = {**{"columns": columns}, **filterset.form.fields}

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
        so we can set the paginate_by and the table_pagination value as attribute of the table.
        """
        self.paginate_by = getattr(table, "paginate_by", None)
        self.table_pagination = getattr(table, "table_pagination", None)
        return super().get_table_pagination(table)


class Detail(GenericModelMixin, PermissionRequiredMixin, DetailView):
    """
    Detail view for a generic model.
    Access requires the `<model>_view` permission.
    """

    permission_action_required = "view"


class Create(
    GenericModelMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
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
            self.model, "_create_success_message.html"
        )
        template = select_template(message_templates)
        return template.render({"object": self.object})

    def get_success_url(self):
        return self.object.get_create_success_url()


class Delete(GenericModelMixin, PermissionRequiredMixin, DeleteView):
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
    GenericModelMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
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
            self.model, "_update_success_message.html"
        )
        template = select_template(message_templates)
        return template.render({"object": self.object})

    def get_success_url(self):
        return self.object.get_update_success_url()


class Duplicate(GenericModelMixin, PermissionRequiredMixin, View):
    permission_action_required = "add"

    def get(self, request, *args, **kwargs):
        source_obj = get_object_or_404(self.model, pk=kwargs["pk"])
        newobj = source_obj.duplicate()

        message_templates = template_names_via_mro(
            self.model, "_duplicate_success_message.html"
        )
        template = select_template(message_templates)
        messages.success(request, template.render({"object": source_obj}))
        return redirect(newobj.get_edit_url())


class Autocomplete(
    GenericModelMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView
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
        # `create_field` is, because we use create_object_from_uri anyway.
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
            return create_object_from_uri(
                value, self.queryset.model, raise_on_fail=True
            )
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
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return http.JsonResponse({"error": str(e)})


class Import(GenericModelMixin, PermissionRequiredMixin, FormView):
    template_name = "generic/generic_import_form.html"
    template_name_suffix = "_import"
    permission_action_required = "add"

    def get_form_class(self):
        form_modules = module_paths(self.model, path="forms", suffix="ImportForm")
        form_class = first_member_match(form_modules, GenericImportForm)
        return modelform_factory(self.model, form_class)

    def form_valid(self, form):
        self.object = form.cleaned_data["url"]
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class SelectMergeOrEnrich(GenericModelMixin, PermissionRequiredMixin, FormView):
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
        kwargs["instance"] = self.get_object()
        return kwargs


class MergeWith(GenericModelMixin, PermissionRequiredMixin, FormView):
    """
    Generic merge view.
    """

    permission_action_required = "change"
    form_class = GenericMergeWithForm
    template_name = "generic/generic_merge.html"

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


class Enrich(GenericModelMixin, PermissionRequiredMixin, FormView):
    """
    Enrich an entity with data from an external source
    If so, it uses the proper Importer to get the data from the Uri and
    provides the user with a form to select the fields that should be updated.
    """

    permission_action_required = "change"
    template_name = "generic/generic_enrich.html"
    form_class = GenericEnrichForm
    importer_class = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.object = get_object_or_404(self.model, pk=self.kwargs["pk"])
        self.uri = self.request.GET.get("uri")
        if not self.uri:
            messages.error(self.request, "No uri parameter specified.")
        self.importer_class = get_importer_for_model(self.model)

    def get(self, *args, **kwargs):
        if self.uri.isdigit():
            return redirect(self.object.get_merge_url(self.uri))
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
            importer = self.importer_class(self.uri, self.model)
            kwargs["data"] = importer.get_data()
        except ImproperlyConfigured as e:
            messages.error(self.request, e)
        return kwargs

    def form_valid(self, form):
        """
        Go through all the form fields and extract the ones that
        start with `update_` and that are set (those are the checkboxes that
        select which fields to update).
        Then use the importers `import_into_instance` method to set those
        fields values on the model instance.
        """
        update_fields = [
            key.removeprefix("update_")
            for (key, value) in self.request.POST.items()
            if key.startswith("update_") and value
        ]
        importer = self.importer_class(self.uri, self.model)
        importer.import_into_instance(self.object, fields=update_fields)
        messages.info(self.request, f"Updated fields {update_fields}")
        content_type = ContentType.objects.get_for_model(self.model)
        uri, created = Uri.objects.get_or_create(
            uri=importer.get_uri,
            content_type=content_type,
            object_id=self.object.id,
        )
        if created:
            messages.info(self.request, f"Added uri {self.uri} to {self.object}")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
