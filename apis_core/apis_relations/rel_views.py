from django.conf import settings
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig

from apis_core.apis_entities.views import GenericListViewNew

from apis_core.apis_relations.models import Triple, Property
from .rel_filters import TripleFilter, PropertyFilter
from .tables import TripleTable, PropertyTable


class GenericRelationView(GenericListViewNew):

    context_filter_name = "filter"
    paginate_by = 25
    template_name = getattr(settings, "APIS_LIST_VIEW_TEMPLATE", "generic_list.html")

    def get_queryset(self, **kwargs):
        self.entity = self.kwargs.get("entity")
        # qs = AbstractRelation.get_relation_class_of_name(self.entity).objects.all()
        qs = None
        # Note: the column by which to sort a table by default can also be defined
        # via a table's order_by field, which will override whatever value order_field
        # is set to, but Django needs order_field to be set to *something* so as not
        # to complain about the queryset missing ordering ("unordered object_list")
        order_field = "id"

        # self.filter = get_generic_relation_filter(
        #     self.entity.title())(self.request.GET, queryset=qs)

        if self.entity == "property":
            self.filter = PropertyFilter(self.request.GET, queryset=qs)
            order_field = "subj_class"
        else:
            self.filter = TripleFilter(self.request.GET, queryset=qs)

        self.filter.form.helper = self.formhelper_class()
        if callable(getattr(self.filter.qs, "filter_for_user", None)):
            return self.filter.qs.filter_for_user().distinct().order_by(order_field)
        else:
            return self.filter.qs.distinct().order_by(order_field)

    def get_table(self, **kwargs):
        # relation_name = self.kwargs["entity"].lower()
        if self.entity == "property":
            self.table_class = PropertyTable
        else:
            self.table_class = TripleTable
        table = super(GenericListViewNew, self).get_table()
        RequestConfig(
            self.request, paginate={"page": 1, "per_page": self.paginate_by}
        ).configure(table)
        return table


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
