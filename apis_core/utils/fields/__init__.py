from django.db.models import DateTimeField, CharField
from apis_core.utils import DateParser


class StringDateTimeField(CharField):
    def pre_save(self, model_instance, add):
        name = self.attname.removesuffix("_string")
        value = getattr(model_instance, self.attname)
        _middle, _from, _to = DateParser.parse_date(value)
        if hasattr(model_instance, f"{name}_datetime_middle"):
            setattr(model_instance, f"{name}_datetime", _middle)
        if hasattr(model_instance, f"{name}_datetime_from"):
            setattr(model_instance, f"{name}_datetime_from", _from)
        if hasattr(model_instance, f"{name}_datetime_to"):
            setattr(model_instance, f"{name}_datetime_to", _to)
        return super().pre_save(model_instance, add)


class TimespanIntervalCharField:
    def contribute_to_class(self, cls, name):
        StringDateTimeField(max_length=255, blank=True, null=True).contribute_to_class(
            cls, f"{name}_string"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime_middle"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime_from"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime_to"
        )
