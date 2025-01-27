import logging
from django.apps import apps
from django import forms
import django_filters
from django_filters.filterset import FilterSet
from django.contrib.contenttypes.models import ContentType

from .forms import GenericFilterSetForm

logger = logging.getLogger(__name__)


class BooleanMultiWidget(forms.MultiWidget):
    attrs = {"class": "form-control form-check-inline"}
    def decompress(self, value):
        return [value, value]


class IncludeExcludeField(forms.MultiValueField):
    def __init__(self, field, *args, **kwargs):
        fields = (field, forms.BooleanField(attrs = {"class": "form-control form-check-inline"}))
        kwargs["widget"] = BooleanMultiWidget(widgets=[f.widget for f in fields])
        super().__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list


class CollectionsFilter(django_filters.filters.QuerySetRequestMixin, django_filters.Filter):
    field_class = django_filters.fields.ModelMultipleChoiceField

    @property
    def field(self):
        return IncludeExcludeField(self.field_class(queryset=self.queryset))

    def filter(self, queryset, value):
        value, filex = value
        if value:
            content_type = ContentType.objects.get_for_model(queryset.model)
            try:
                skoscollectioncontentobject = apps.get_model("collections.SkosCollectionContentObject")
                scco = skoscollectioncontentobject.objects.filter(content_type=content_type, collection__in=value).values("object_id")
                if filex:
                    return queryset.exclude(id__in=scco)
                return queryset.filter(id__in=scco)
            except LookupError as e:
                logger.debug("Not filtering for collections: %s", e)
        return queryset


class GenericFilterSet(FilterSet):
    """
    Our GenericFilterSet sets the default `form` to be our
    GenericFilterSetForm, which is set up to ignore the `columns` field
    of the form.
    """

    class Meta:
        form = GenericFilterSetForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            skoscollection = apps.get_model("collections.SkosCollection")
            self.filters["collections"] = CollectionsFilter(queryset=skoscollection.objects.all(), lookup_choices = [("exclude"), ("include")])
        except LookupError as e:
            logger.debug("Not adding collections filter to form: %s", e)
