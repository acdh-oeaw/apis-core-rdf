from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CustomLogEntryManager(models.Manager):
    def log_action(self, user, obj=None, message="", metadata={}):
        username = "System action"
        if user:
            username = str(user)
        entry = self.model.objects.create(user=username)
        if obj:
            content_type = ContentType.objects.get_for_model(obj)
            entry.content_type = content_type
            natural_key = f"{content_type.app_label}.{content_type.name}"
            metadata["natural_key"] = natural_key
            message += f" {natural_key}: {obj}"
            metadata["pk"] = obj.pk
            if hasattr(obj, "id"):
                entry.object_id = obj.id
        if message:
            entry.message = message
        if metadata:
            entry.metadata = metadata
        entry.save()

    def add_something(self, user, obj):
        message = f"{user} added"
        metadata = {"type": "add"}
        self.log_action(user, obj, message, metadata)

    def delete_something(self, user, obj):
        message = f"{user} deleted"
        metadata = {"type": "del"}
        self.log_action(user, obj, message, metadata)

    def change_something(self, user, obj, update_fields=[]):
        message = f"{user} changed"
        metadata = {"type": "change", "update_fields": update_fields}
        self.log_action(user, obj, message, metadata)


class CustomLogEntry(models.Model):
    """
    A custom LogEntry model. Django has its own contrib.admin.LogEntry, but that
    is primarily used for actions in the admin area. Using a custom LogEntry we
    are more flexible.
    """

    user = models.CharField(max_length=150, editable=False)
    action_time = models.DateTimeField(auto_now_add=True, editable=False)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    message = models.TextField(null=True)
    metadata = models.JSONField(null=True)

    objects = CustomLogEntryManager()

    class Meta:
        ordering = ["-action_time"]
