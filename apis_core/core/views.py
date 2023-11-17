from django.views.generic.list import ListView
from django.contrib.contenttypes.models import ContentType
from reversion.models import Revision, Version


class Versions(ListView):
    paginate_by = 100
    model = Version
    instance = None

    def dispatch(self, request, *args, **kwargs):
        if content_type := kwargs.get("content_type"):
            contenttype = ContentType.objects.get_for_id(content_type)
            if object_id := kwargs.get("object_id"):
                self.instance = contenttype.model_class().objects.get(pk=object_id)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.instance:
            return Version.objects.get_for_object(self.instance)
        return Version.objects.all()
