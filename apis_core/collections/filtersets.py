from django.contrib.contenttypes.models import ContentType

from apis_core.collections.models import SkosCollectionContentObject
from apis_core.generic.filtersets import GenericFilterSet


class SkosCollectionContentObjectFilterSet(GenericFilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "collections" in self.filters:
            del self.filters["collections"]
        content_types = SkosCollectionContentObject.objects.all().values("content_type")
        self.filters["content_type"].queryset = ContentType.objects.filter(
            pk__in=content_types
        )
