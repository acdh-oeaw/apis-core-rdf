from django.db.models import DateTimeField, CharField


class StringDateTimeField(CharField):
    """A simple CharField, that populates datetime fields with its own value"""

    def pre_save(self, model_instance, add):
        name = self.attname.removesuffix("_string")
        value = getattr(model_instance, self.attname)
        if hasattr(model_instance, f"{name}_datetime"):
            setattr(model_instance, f"{name}_datetime", value)
        if hasattr(model_instance, f"{name}_datetime_from"):
            setattr(model_instance, f"{name}_datetime_from", value)
        if hasattr(model_instance, f"{name}_datetime_to"):
            setattr(model_instance, f"{name}_datetime_to", value)
        return super().pre_save(model_instance, add)


class DateTimeIntervalCharField:
    def contribute_to_class(self, cls, name):
        StringDateTimeField(max_length=255, blank=True, null=True).contribute_to_class(
            cls, f"{name}_string"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime_from"
        )
        DateTimeField(editable=False, blank=True, null=True).contribute_to_class(
            cls, f"{name}_datetime_to"
        )
