from django.conf import settings


def access_for_all(self, viewtype="list"):
    if self.request.user.is_authenticated:
        return self.request.user.is_authenticated
    match viewtype:
        case "list":
            return getattr(settings, "APIS_LIST_VIEWS_ALLOWED", False)
        case "detail":
            return getattr(settings, "APIS_DETAIL_VIEWS_ALLOWED", False)
    return False


def access_for_all_function(user):
    if user.is_anonymous:
        return getattr(settings, "APIS_DETAIL_VIEWS_ALLOWED", False)
    else:
        return True


ENTITIES_DEFAULT_COLS = [
    "start_date",
    "start_date_written",
    "end_date",
    "end_date_written",
    "text",
    "collection",
    "status",
    "source",
    "references",
    "notes",
]


def get_child_classes(objids, obclass, labels=False):
    """used to retrieve a list of primary keys of sub classes"""
    if labels:
        labels_lst = []
    for obj in objids:
        obj = obclass.objects.get(pk=obj)
        p_class = list(obj.vocabsbaseclass_set.all())
        p = p_class.pop() if len(p_class) > 0 else False
        while p:
            if p.pk not in objids:
                if labels:
                    labels_lst.append((p.pk, p.label))
                objids.append(p.pk)
            p_class += list(p.vocabsbaseclass_set.all())
            p = p_class.pop() if len(p_class) > 0 else False
    if labels:
        return (objids, labels_lst)
    else:
        return objids


def get_python_safe_module_path(instance: object):
    """
    return a python safe version of the full path of an object
    this can for example be used as a method name
    """
    modulepath = get_module_path(instance)
    return modulepath.replace(".", "_")


def get_module_path(instance: object):
    """
    return the full path to the class of an object
    """
    instance_type = type(instance)
    module = instance_type.__module__
    name = instance_type.__name__
    return f"{module}.{name}"
