from django.contrib.contenttypes.models import ContentType
from apis_core.apis_metainfo.models import RootObject

def get_all_contenttype_classes():
    contenttype_classes = list(ContentType.objects.all())
    contenttype_classes = [x.model_class() for x in contenttype_classes]
    contenttype_classes = list(filter(None, contenttype_classes))
    apis_core_classes = [x for x in contenttype_classes if x.__module__.startswith("apis_core")]
    apis_child_classes = [x for x in contenttype_classes if issubclass(x, RootObject)]
    all_classes = apis_core_classes + apis_child_classes
    all_classes.append(ContentType)
    all_classes = [x for x in all_classes if not x.__module__.startswith("apis_core.apis_labels")]
    all_classes = list(set(all_classes))
    all_classes = sorted(all_classes, key=lambda x: x.__module__)
    return all_classes
