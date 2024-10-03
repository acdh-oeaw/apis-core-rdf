from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView

from apis_core.generic.views import Create
from apis_core.relations.templatetags.relations import (
    possible_relation_types_from,
    relations_from,
)


class CreateRelation(Create):
    def get_form_kwargs(self, *args, **kwargs) -> dict:
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

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        self.reverse = self.request.GET.get("reverse", "false").lower() == "true"

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self.model)
        resp["HX-Trigger-After-Settle"] = (
            '{"reinit_select2": "relation_' + content_type.model + '_form"}'
        )
        return resp

    def get_form_kwargs(self, *args, **kwargs) -> dict:
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["reverse"] = self.reverse
        content_type = ContentType.objects.get_for_model(self.model)
        kwargs["hx_post_route"] = reverse(
            "apis_core:relations:create_relation_form", args=[content_type]
        )
        return kwargs

    def get_success_url(self) -> str:
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
        return reverse("apis_core:relations:list_relations", args=args)


class ListRelations(TemplateView):
    template_name = "relations/list_relations.html"

    def get_context_data(self, *args, **kwargs) -> dict:
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
