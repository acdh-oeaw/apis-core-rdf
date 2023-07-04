from django.http import Http404
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from apis_core.utils import helpers


class EntityMixin:
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if "entity" in kwargs:
            self.entity = kwargs.get("entity")
            self.entity_model = helpers.get_entity_class_by_name(self.entity)
        else:
            raise Http404(_("No `entity` found in the path"))


class EntityInstanceMixin(EntityMixin):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if "pk" in kwargs:
            self.pk = kwargs.get("pk")
        else:
            raise Http404(_("No `pk` found in the path"))
        self.instance = get_object_or_404(self.entity_model, pk=self.pk)
