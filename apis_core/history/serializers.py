from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class ModelChangeSerializer(serializers.Serializer):
    field = serializers.CharField()
    old = serializers.SerializerMethodField(method_name="get_field_data_old")
    new = serializers.SerializerMethodField(method_name="get_field_data_new")

    def get_data_for_m2m_field(self, value, field):
        sst = [
            str(obj2)
            for obj2 in field.related_model.objects.filter(
                pk__in=[obj3[field.attname] for obj3 in value]
            )
        ]
        return " | ".join(sst)

    def get_field_data(self, obj, new: bool):
        if new:
            value = obj.new
        else:
            value = obj.old
        if obj.field in [x.name for x in self._parent_object._meta.local_fields]:
            field = self._parent_object._meta.get_field(obj.field)
            if field.is_relation and value is not None:
                return str(getattr(self._args[1], obj.field))
            return value
        else:
            for field in self._parent_object._history_m2m_fields:
                if field.attname == obj.field:
                    return self.get_data_for_m2m_field(value, field)
        return obj

    def get_field_data_new(self, obj):
        repr = self.get_field_data(obj, True)
        return repr

    def get_field_data_old(self, obj):
        repr = self.get_field_data(obj, False)
        return repr

    def __init__(self, instance=None, parent_object=None, **kwargs):
        self._parent_object = parent_object
        super().__init__(instance, **kwargs)


class HistoryLogSerializer(serializers.Serializer):
    diff = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(source="history_date")
    version_tag = serializers.CharField()
    user = serializers.CharField(source="history_user")
    action = serializers.SerializerMethodField()
    model = serializers.CharField(source="instance.__class__.__name__")
    module = serializers.CharField(source="instance.__class__._meta.app_label")
    instance = serializers.CharField()
    object_id = serializers.IntegerField(source="id")
    history_id = serializers.IntegerField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_diff(self, obj):
        if obj.history_type == "-":
            return None
        changed_fields = []
        changes = []
        for change in obj.get_diff():
            changed_fields.append(change.field)
            changes.append(ModelChangeSerializer(change, obj).data)
        return {"changed_fields": changed_fields, "changes": changes}

    def get_action(self, obj) -> str:
        match obj.history_type:
            case "+":
                return "created"
            case "~":
                return "changed"
            case "-":
                return "deleted"


class HistoryObjectSerializer(serializers.Serializer):
    history = serializers.SerializerMethodField()
    model = serializers.CharField(source="__class__.__name__")
    module = serializers.CharField(source="_meta.app_label")
    instance = serializers.SerializerMethodField()
    object_id = serializers.IntegerField(source="id")

    def get_instance(self, obj) -> str:
        return str(obj)

    @extend_schema_field(HistoryLogSerializer(many=True))
    def get_history(self, obj):
        return HistoryLogSerializer(obj.get_history_data(), many=True).data
