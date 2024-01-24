from apis_core.generic.filtersets import GenericFilterSet, GenericFilterSetForm
from django_filters import CharFilter

PROPERTY_EXCLUDES = ["self_contenttype", "name", "property_class_uri", "rootobject_ptr"]


class PropertyFilterSetForm(GenericFilterSetForm):
    columns_exclude = PROPERTY_EXCLUDES


class PropertyFilterSet(GenericFilterSet):
    name_forward = CharFilter(lookup_expr="icontains")
    name_reverse = CharFilter(lookup_expr="icontains")

    class Meta:
        form = PropertyFilterSetForm
        exclude = PROPERTY_EXCLUDES


class TripleFilterSet(GenericFilterSet):
    subj = CharFilter(method="subj_icontains")
    obj = CharFilter(method="obj_icontains")

    def subj_icontains(self, queryset, name, value):
        return queryset.filter(subj__name__icontains=value)

    def obj_icontains(self, queryset, name, value):
        return queryset.filter(obj__name__icontains=value)
