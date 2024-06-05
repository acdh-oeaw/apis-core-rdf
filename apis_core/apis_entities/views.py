from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.html import format_html
from django.views import View
from django.views.generic.edit import FormView

from apis_core.generic.views import GenericModelMixin, Update
from apis_core.apis_entities.forms import EntitiesMergeForm


class EntitiesUpdate(Update):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["mergeform"] = EntitiesMergeForm(instance=self.get_object())
        return context


class EntitiesDuplicate(GenericModelMixin, PermissionRequiredMixin, View):
    permission_action_required = "create"

    def get(self, request, *args, **kwargs):
        source_obj = get_object_or_404(self.model, pk=kwargs["pk"])
        newobj = source_obj.duplicate()

        messages.success(
            request,
            format_html(
                "<a href={}>{}</a> was successfully duplicated to the current object:",
                source_obj.get_absolute_url(),
                source_obj,
            ),
        )
        return redirect(
            reverse(
                "apis:apis_entities:generic_entities_edit_view",
                kwargs={
                    "pk": newobj.id,
                    "contenttype": newobj.__class__.__name__.lower(),
                },
            )
        )


class EntitiesMerge(GenericModelMixin, PermissionRequiredMixin, FormView):
    permission_action_required = "create"
    form_class = EntitiesMergeForm
    template_name = "entity_merge.html"
    template_name_suffix = "_merge"

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

    def form_valid(self, form):
        obj = self.get_object()
        other = form.cleaned_data["uri"]
        obj.merge_with([other])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "apis:apis_entities:generic_entities_edit_view",
            args=[self.get_object().__class__.__name__.lower(), self.get_object().id],
        )
