from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic.base import TemplateView
from django.views.generic.detail import BaseDetailView

from apis_core.generic.helpers import split_and_strip_parameter, string_to_bool
from apis_core.generic.templatetags.generic import content_types_by_natural_keys
from apis_core.generic.views import Create, GenericModelMixin
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


class RelationParamsMixin:
    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        self.params = self.request.GET.dict()
        self.params["reverse"] = string_to_bool(self.params.get("reverse", "false"))
        self.params["relation_types"] = split_and_strip_parameter(
            self.request.GET.getlist("relation_types")
        )


class CreateRelationForm(RelationParamsMixin, CreateRelation):
    template_name = "relations/create_relation_form.html"

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(self.model)
        resp["HX-Trigger-After-Settle"] = (
            '{"reinit_select2": "relation_' + content_type.model + '_form"}'
        )
        return resp

    def get_form_kwargs(self, *args, **kwargs) -> dict:
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["params"] = self.params
        content_type = ContentType.objects.get_for_model(self.model)
        kwargs["params"]["hx_post_route"] = reverse(
            "apis_core:relations:create_relation_form", args=[content_type]
        )
        return kwargs

    def get_success_url(self) -> str:
        obj = self.object.obj if self.params["reverse"] else self.object.subj
        args = [obj.content_type, obj.id]
        params = {
            k: self.params[k] for k in ["relation_types", "replace_id", "table_suffix"]
        }
        params = "?" + urlencode(params, doseq=True)
        return reverse("apis_core:relations:list_relations", args=args) + params


class ListRelations(
    RelationParamsMixin, GenericModelMixin, BaseDetailView, TemplateView
):
    template_name = "relations/partials/list_relations.html"

    def get_context_data(self, *args, **kwargs) -> dict:
        ctx = super().get_context_data(*args, **kwargs)
        ctx["relations"] = []

        relation_types = content_types_by_natural_keys(
            tuple(self.params["relation_types"])
        )
        if not relation_types:
            relation_types = possible_relation_types_from(self.object)
        for relation_type in relation_types:
            ctx["relations"].extend(relations_from(self.object, relation_type))

        ctx.update(self.params)

        return ctx

    def get(self, *args, **kwargs):
        resp = super().get(*args, **kwargs)
        resp["HX-Trigger"] = "dismissModal"
        return resp
