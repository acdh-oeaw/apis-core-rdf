import logging

import django_filters
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django_filters.filterset import FilterSet

from apis_core.generic.forms.fields import IncludeExcludeField

from .forms import GenericFilterSetForm

logger = logging.getLogger(__name__)


class CollectionsFilter(django_filters.filters.ModelMultipleChoiceFilter):
    """
    A simple filter for connections to collections. It provides an `include`/`exclude`
    selector, which allows to define what the filter should do.
    """

    @property
    def field(self):
        return IncludeExcludeField(super().field, required=self.extra["required"])

    def filter(self, queryset, value):
        try:
            value, include_exclude = value
        except ValueError:
            pass
        if value:
            content_type = ContentType.objects.get_for_model(queryset.model)
            try:
                skoscollectioncontentobject = apps.get_model(
                    "collections.SkosCollectionContentObject"
                )
                scco = skoscollectioncontentobject.objects.filter(
                    content_type=content_type, collection__in=value
                ).values("object_id")
                match include_exclude:
                    case "include":
                        return queryset.filter(id__in=scco)
                    case "exclude":
                        return queryset.exclude(id__in=scco)
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
        # we set the UnknownFieldBehavior to WARN, so the form does not
        # break if there are JSONFields
        unknown_field_behavior = django_filters.UnknownFieldBehavior.WARN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            skoscollection = apps.get_model("collections.SkosCollection")
            if skoscollection.objects.exists():
                self.filters["collections"] = CollectionsFilter(
                    queryset=skoscollection.objects.all(),
                )
        except LookupError as e:
            logger.debug("Not adding collections filter to form: %s", e)
