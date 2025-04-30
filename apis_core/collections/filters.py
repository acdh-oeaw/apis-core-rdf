import logging

import django_filters
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from apis_core.generic.forms.fields import RowColumnMultiValueField

logger = logging.getLogger(__name__)


class CollectionsIncludeExcludeFilter(django_filters.filters.ModelMultipleChoiceFilter):
    """
    The CollectionsIncludeExcludeFilter provides to ModelMultipleChoiceFilters that allow
    to filter model instances that are either **in** a collection OR (or AND) are **not in**
    a collection.
    """

    @property
    def field(self):
        return RowColumnMultiValueField(
            fields=[super().field, super().field],
            labels=["include", "exclude"],
            required=self.extra["required"],
        )

    def filter(self, queryset, value):
        if not value:
            return queryset
        include = exclude = []
        q = Q()
        try:
            content_type = ContentType.objects.get_for_model(queryset.model)
            skoscollectioncontentobject = apps.get_model(
                "collections.SkosCollectionContentObject"
            )
            include, exclude = value
            include_ids = skoscollectioncontentobject.objects.filter(
                content_type=content_type, collection__in=include
            ).values("object_id")
            if include:
                q &= Q(pk__in=include_ids)
            exclude_ids = skoscollectioncontentobject.objects.filter(
                content_type=content_type, collection__in=exclude
            ).values("object_id")
            if exclude:
                q &= ~Q(pk__in=exclude_ids)
        except LookupError as e:
            logger.debug("Not filtering for collections: %s", e)
        return queryset.filter(q)
