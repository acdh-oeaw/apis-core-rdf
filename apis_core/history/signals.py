from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone


@receiver(pre_delete)
def set_history_date(sender, instance, using, origin, **kwargs):
    if getattr(instance, "_history_date", None) is None:
        instance._history_date = timezone.now()
