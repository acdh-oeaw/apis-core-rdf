from apis_core.generic.views import Create
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.forms import modelform_factory

from apis_core.relations.templatetags.relations import (
    relations_from,
    possible_relation_types_from,
)
from apis_core.relations.forms import RelationFormHX


class CreateRelation(Create):
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["initial"]["obj_content_type"] = self.request.GET.get("obj_content_type")
        kwargs["initial"]["obj_object_id"] = self.request.GET.get("obj_object_id")
        kwargs["initial"]["subj_content_type"] = self.request.GET.get(
            "subj_content_type"
        )
        kwargs["initial"]["subj_object_id"] = self.request.GET.get("subj_object_id")
        return kwargs


class CreateRelationForm(CreateRelation):
    template_name = "relations/create_relation_form.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.reverse = self.request.GET.get("reverse", "false").lower() == "true"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["reverse"] = self.reverse
        return kwargs

    def get_success_url(self):
        args = [
            self.object.obj_content_type,
            self.object.subj_content_type,
            self.object.subj_object_id,
        ]
        if self.reverse:
            args = [
                self.object.subj_content_type,
                self.object.obj_content_type,
                self.object.obj_object_id,
            ]
        return reverse("apis_core:list_relations", args=args)

    def get_form_class(self, *args, **kwargs):
        return modelform_factory(self.model, RelationFormHX)


class ListRelations(TemplateView):
    template_name = "relations/list_relations.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["target"] = kwargs.get("target_contenttype")
        ctx["object"] = get_object_or_404(
            kwargs.get("object_contenttype").model_class(), pk=kwargs.get("object_id")
        )
        ctx["relations"] = relations_from(ctx["object"])
        ctx["possible_relations"] = possible_relation_types_from(ctx["object"])
        ctx["edit"] = True
        return ctx

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        resp["HX-Trigger"] = "dismissModal"
        return resp
