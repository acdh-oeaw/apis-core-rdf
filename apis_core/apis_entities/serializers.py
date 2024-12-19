from rdflib import Literal, URIRef
from rdflib.namespace import RDF, RDFS
from rest_framework import serializers

from apis_core.generic.serializers import (
    GenericHyperlinkedIdentityField,
    GenericModelCidocSerializer,
)
from apis_core.generic.utils.rdf_namespace import APPELLATION, CRM


class MinimalEntitySerializer(serializers.Serializer):
    uri = GenericHyperlinkedIdentityField(
        view_name="apis_core:generic:genericmodelapi-detail"
    )
    name = serializers.SerializerMethodField(method_name="get_name")

    def get_name(self, object) -> str:
        return str(object)


class E21_PersonCidocSerializer(GenericModelCidocSerializer):
    def to_representation(self, instance):
        g = super().to_representation(instance)

        g.add((self.instance_uri, RDF.type, CRM.E21_Person))

        if hasattr(instance, "forename"):
            forename_uri = URIRef(APPELLATION[f"forename_{instance.id}"])
            g.add(
                (
                    forename_uri,
                    RDF.type,
                    CRM.E33_E41_Linguistic_Appellation,
                )
            )
            g.add(
                (
                    self.appellation_uri,
                    CRM.P106_is_composed_of,
                    forename_uri,
                )
            )
            g.add((forename_uri, RDFS.label, Literal(instance.forename)))

        if hasattr(instance, "surname"):
            surname_uri = URIRef(APPELLATION[f"surname_{instance.id}"])
            g.add(
                (
                    surname_uri,
                    RDF.type,
                    CRM.E33_E41_Linguistic_Appellation,
                )
            )
            g.add(
                (
                    self.appellation_uri,
                    CRM.P106_is_composed_of,
                    surname_uri,
                )
            )
            g.add((surname_uri, RDFS.label, Literal(instance.surname)))

        return g
