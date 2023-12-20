from rest_framework import serializers
from rest_framework.fields import empty
from django.core.exceptions import FieldDoesNotExist


class ModelChangeSerializer(serializers.Serializer):
    field = serializers.CharField()
    old = serializers.SerializerMethodField(method_name="get_field_data_old")
    new = serializers.SerializerMethodField(method_name="get_field_data_new")

    def get_field_data(self, obj):
        try:
            self._parent_object._meta.get_field(obj["field"])
            return obj["value"]
        except FieldDoesNotExist:
            for field in self._parent_object._history_m2m_fields:
                if field.attname == obj["field"]:
                    sst = [
                        str(obj2)
                        for obj2 in field.related_model.objects.filter(
                            pk__in=[obj3[obj["field"]] for obj3 in obj["value"]]
                        )
                    ]
                    return " | ".join(sst)
        return obj

    def get_field_data_new(self, obj):
        repr = self.get_field_data({"field": obj.field, "value": obj.new})
        return repr

    def get_field_data_old(self, obj):
        repr = self.get_field_data({"field": obj.field, "value": obj.old})
        return repr

    def __init__(self, instance=None, parent_object=None, **kwargs):
        self._parent_object = parent_object
        super().__init__(instance, **kwargs)


class HistoryLogSerializer(serializers.Serializer):
    diff = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(source="history_date")
    version_tag = serializers.CharField()
    user = serializers.CharField(source="history_user")

    def get_diff(self, obj):
        if obj.prev_record is None:
            return []
        diff = obj.diff_against(obj.prev_record)
        changed_fields = []
        changes = []
        for change in diff.changes:
            if change.new == "" and change.old == None:
                continue
            changed_fields.append(change.field)
            changes.append(ModelChangeSerializer(change, obj).data)
        return {"changed_fields": changed_fields, "changes": changes}
