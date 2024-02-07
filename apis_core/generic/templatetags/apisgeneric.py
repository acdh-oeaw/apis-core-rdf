from itertools import chain

from django import template
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.filter
def contenttype(model):
    return ContentType.objects.get_for_model(model)


@register.simple_tag
def modeldict(instance, fields=None, exclude=None):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, "editable", False):
            continue
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        field = instance._meta.get_field(f.name)
        data[field] = instance._get_FIELD_display(field)
        if getattr(field, "remote_field", False):
            data[field] = getattr(instance, field.name)
        if getattr(field, "m2m_field_name", False):
            values = getattr(instance, field.name).all()
            data[field] = ", ".join([str(value) for value in values])
    return data


@register.simple_tag
def contenttypes(app_labels=None):
    if app_labels:
        app_labels = app_labels.split(",")
        return ContentType.objects.filter(app_label__in=app_labels)
    return ContentType.objects.all()
