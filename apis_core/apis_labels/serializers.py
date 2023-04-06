from rest_framework import serializers

from .models import Label


class LabelSerializerLegacy(serializers.ModelSerializer):
    # TODO RDF: Check if this should be removed or adapted
    # from apis_core.apis_vocabularies.serializers import LabelTypeMinimalSerializer
    # label_type = LabelTypeMinimalSerializer()

    class Meta:
        model = Label
        fields = ("id", "label", "isoCode_639_3", "label_type")
