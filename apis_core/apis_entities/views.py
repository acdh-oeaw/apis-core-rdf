from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import format_html
from django.views import View

from apis_core.apis_metainfo.models import RootObject
from apis_core.generic.helpers import generate_search_filter
from apis_core.generic.views import GenericModelMixin


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
        return redirect(newobj.get_edit_url())


class EntitiesAutocomplete(autocomplete.Select2QuerySetView):
    """
    This endpoint allows us to use autocomplete over multiple model classes.
    It takes a parameter `entities` which is a list of ContentType natural
    keys and searches for the query in all instances of those entities
    (using `generate_search_filter`, which means it uses a different search
    approach for every model).
    The return values of the endpoint are then prefixed with the id of the
    contenttype of the results, separated by an underscore.

    Example:
    Using this endpoint with the parameters:

        ?entities=apis_ontology.person&entities=apis_ontology.place&q=ammer

    gives you all the persons and places that have `ammer` in their names
    and labels.
    """

    def get_result_value(self, result) -> str:
        content_type = ContentType.objects.get_for_model(result)
        return f"{content_type.id}_" + super().get_result_value(result)

    def get_queryset(self):
        q = Q()
        if entities := self.request.GET.getlist("entities"):
            for entity in entities:
                app_label, model = entity.split(".")
                content_type = get_object_or_404(
                    ContentType, app_label=app_label, model=model
                )
                name = (
                    RootObject.objects_inheritance.get_queryset()._get_ancestors_path(
                        content_type.model_class()
                    )
                )
                q |= Q(**{f"{name}__isnull": False}) & generate_search_filter(
                    content_type.model_class(), self.q, prefix=f"{name}__"
                )
        return RootObject.objects_inheritance.select_subclasses().filter(q)
