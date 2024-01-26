from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crum import get_current_request

from .models import CustomLogEntry


@receiver(post_save)
def log_save(sender, instance, created, raw, using, update_fields, **kwargs):
    if sender is CustomLogEntry:
        return
    user = None
    request = get_current_request()
    if request:
        user = request.user
    if created:
        CustomLogEntry.objects.add_something(user, instance)
    else:
        if update_fields:
            update_fields = list(update_fields)
        CustomLogEntry.objects.change_something(user, instance, update_fields)


@receiver(post_delete)
def log_delete(sender, instance, using, origin, **kwargs):
    if sender is CustomLogEntry:
        return
    user = None
    request = get_current_request()
    if request:
        user = request.user
    CustomLogEntry.objects.delete_something(user, instance)
