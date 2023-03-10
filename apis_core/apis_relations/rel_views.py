from django.conf import settings
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig
from apis_core.apis_entities.views import GenericListViewNew
from apis_core.apis_relations.models import Triple, Property


# TODO RDF: Check if this should be removed or adapted
class GenericRelationDetailView(DetailView):

    template_name = getattr(
        settings,
        "APIS_RELATIONS_DETAIL_VIEW_TEMPLATE",
        "apis_relations/relations_detail_generic.html",
    )

    def get_object(self):
        entity = self.kwargs["entity"].lower()
        instance = self.kwargs["pk"].lower()
        # entity_model = AbstractRelation.get_relation_class_of_name(entity)
        if entity == "property":
            instance = Property.objects.get(pk=instance)
        else:
            instance = Triple.objects.get(pk=instance)
        return instance

    def get_context_data(self, **kwargs):
        context = super(GenericRelationDetailView, self).get_context_data()
        context["entity"] = self.kwargs["entity"].lower()
        context["entity_type"] = context["entity"]
        return context
