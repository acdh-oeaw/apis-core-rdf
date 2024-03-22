from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    Serializer,
    CharField,
    IntegerField,
)
from rest_framework.reverse import reverse


class GenericHyperlinkedRelatedField(HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        contenttype = ContentType.objects.get_for_model(obj, for_concrete_model=True)
        url_kwargs = {"contenttype": contenttype, "pk": obj.pk}
        return reverse(
            "apis_core:generic:genericmodelapi-detail",
            kwargs=url_kwargs,
            request=request,
            format=format,
        )

    def use_pk_only_optimization(self):
        # We have the complete object instance already. We don't need
        # to run the 'only get the pk for this relationship' code.
        return False


class GenericHyperlinkedIdentityField(GenericHyperlinkedRelatedField):
    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, "The `view_name` argument is required."
        kwargs["read_only"] = True
        kwargs["source"] = "*"
        super().__init__(view_name, **kwargs)


class GenericHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    serializer_related_field = GenericHyperlinkedRelatedField
    serializer_url_field = GenericHyperlinkedIdentityField


def serializer_factory(
    model, serializer=GenericHyperlinkedModelSerializer, fields="__all__", **kwargs
):
    defaultmeta = type(str("Meta"), (object,), {"fields": fields})
    meta = getattr(serializer, "Meta", defaultmeta)
    meta.model = model
    serializer = type(
        str("%sModelSerializer" % model._meta.object_name),
        (serializer,),
        {"Meta": meta},
    )
    return serializer


class ContentTypeInstanceSerializer(Serializer):
    id = IntegerField(required=True)
    content_type = CharField(required=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        app_label, model = data.get("content_type").split(".")
        content_type = get_object_or_404(ContentType, app_label=app_label, model=model)
        return get_object_or_404(content_type.model_class(), pk=data.get("id"))
