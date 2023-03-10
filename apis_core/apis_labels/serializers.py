from rest_framework import serializers

# __before_rdf_refactoring__
# from apis_core.apis_vocabularies.serializers import LabelTypeMinimalSerializer
from .models import Label


class LabelSerializerLegacy(serializers.ModelSerializer):

    # __before_rdf_refactoring__
    # label_type = LabelTypeMinimalSerializer()

    class Meta:
        model = Label
        fields = ("id", "label", "isoCode_639_3", "label_type")
