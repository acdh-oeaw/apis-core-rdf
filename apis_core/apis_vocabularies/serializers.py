from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from rest_framework import serializers

from .models import (
    TextType,
    CollectionType,
    VocabsBaseClass,
    VocabNames,
)


###########################################################
#
#  Generic Vocabs Serializer
#
###########################################################


class GenericVocabsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    userAdded = serializers.SerializerMethodField(method_name="add_user")
    parent_class = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    vocab_name = serializers.SerializerMethodField(method_name="add_vocabname")
    name = serializers.CharField()
    label = serializers.CharField()

    def add_user(self, obj):
        print(f"user pk: {obj.userAdded_id}")
        try:
            u = User.objects.get(pk=obj.userAdded_id)
            if u.first_name and u.last_name:
                return f"{u.last_name}, {u.first_name}"
            else:
                return str(u)
        except:
            return ""

    def add_vocabname(self, obj):
        return str(obj.__class__.__name__)

    def __init__(self, *args, **kwargs):
        super(GenericVocabsSerializer, self).__init__(*args, **kwargs)
        if type(self.instance) == QuerySet:
            rt = self.instance[0]
        else:
            rt = self.instance
        if "Relation" in rt.__class__.__name__:
            self.fields["name_reverse"] = serializers.CharField()
            self.fields["label_reverse"] = serializers.CharField()


###########################################################
#
# Meta- Serializers
#
##########################################################


class UserAccSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class VocabsBaseSerializer(serializers.HyperlinkedModelSerializer):
    userAdded = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:user-detail", lookup_field="pk", read_only=True
    )
    parent_class = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:vocabsbaseclass-detail",
        lookup_field="pk",
        read_only=True,
    )
    vocab_name = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:vocabnames-detail", lookup_field="pk", read_only=True
    )


class CollectionTypeSerializer(VocabsBaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="apis:apis_api:collectiontype-detail", lookup_field="pk"
    )

    class Meta:
        fields = "__all__"
        model = CollectionType


class VocabsBaseClassSerializer(VocabsBaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="apis:apis_api:vocabsbaseclass-detail", lookup_field="pk"
    )

    class Meta:
        fields = "__all__"
        model = VocabsBaseClass


class VocabNamesSerializer(VocabsBaseSerializer):
    class Meta:
        fields = "__all__"
        model = VocabNames


############################################################
#
# Entity Types
#
###########################################################


class TextTypeSerializer(VocabsBaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="apis:apis_api:texttype-detail", lookup_field="pk"
    )
    collections = serializers.HyperlinkedRelatedField(
        view_name="apis:apis_api:collection-detail",
        lookup_field="pk",
        many=True,
        read_only=True,
    )

    class Meta:
        fields = "__all__"
        model = TextType


# TODO RDF: Check if this should be removed or adapted
#
# class InstitutionTypeSerializer(VocabsBaseSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name="apis:apis_api:institutiontype-detail",
#         lookup_field="pk"
#     )
#
#     class Meta:
#         fields = '__all__'
#         model = InstitutionType
#
#
# class ProfessionTypeSerializer(VocabsBaseSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name="apis:apis_api:profession-detail",
#         lookup_field="pk"
#     )
#
#     class Meta:
#         fields = '__all__'
#         model = ProfessionType
#
#
# class PlaceTypeSerializer(VocabsBaseSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name="apis:apis_api:placetype-detail",
#         lookup_field="pk"
#     )
#
#     class Meta:
#         fields = '__all__'
#         model = PlaceType
#
#
# class EventTypeSerializer(VocabsBaseSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name="apis:apis_api:eventtype-detail",
#         lookup_field="pk"
#     )
#
#     class Meta:
#         fields = '__all__'
#         model = EventType
#
#
# class WorkTypeSerializer(VocabsBaseSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name="apis:apis_api:worktype-detail",
#         lookup_field="pk"
#     )
#
#     class Meta:
#         fields = '__all__'
#         model = WorkType
#
#
