from rdflib import Literal, Namespace, URIRef
from rdflib.namespace import GEO, RDF, RDFS, XSD
from rest_framework import serializers

from apis_core.generic.serializers import (
    GenericHyperlinkedIdentityField,
    GenericModelCidocSerializer,
)


class MinimalEntitySerializer(serializers.Serializer):
    uri = GenericHyperlinkedIdentityField(
        view_name="apis_core:generic:genericmodelapi-detail"
    )
    name = serializers.SerializerMethodField(method_name="get_name")

    def get_name(self, object) -> str:
        return str(object)


class E53_PlaceCidocSerializer(GenericModelCidocSerializer):
    def to_representation(self, instance):
        g = super().to_representation(instance)

        crm_namespace = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        attributes_namespace = Namespace(f"{self.base_uri}/attributes/")
        g.add((self.instance_uri, RDF.type, crm_namespace.E53_Place))
        if instance.latitude is not None and instance.longitude is not None:
            node_spaceprimitive = attributes_namespace[f"spaceprimitive.{instance.id}"]
            g.add(
                (
                    self.instance_uri,
                    crm_namespace.P168_place_is_defined_by,
                    node_spaceprimitive,
                )
            )
            g.add(
                (
                    node_spaceprimitive,
                    RDF.type,
                    crm_namespace.E94_Space_Primitive,
                )
            )
            g.add(
                (
                    node_spaceprimitive,
                    crm_namespace.P168_place_is_defined_by,
                    Literal(
                        (
                            f"Point ( {'+' if instance.longitude > 0 else ''}{instance.longitude} {'+' if instance.latitude > 0 else ''}{instance.latitude} )"
                        ),
                        datatype=GEO.wktLiteral,
                    ),
                )
            )
        return g


class E21_PersonCidocSerializer(GenericModelCidocSerializer):
    def to_representation(self, instance):
        g = super().to_representation(instance)

        crm_namespace = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
        appellation_namespace = Namespace(f"{self.base_uri}/appellation/")
        attributes_namespace = Namespace(f"{self.base_uri}/attributes/")
        g.add((self.instance_uri, RDF.type, crm_namespace.E21_Person))

        if hasattr(instance, "forename"):
            forename_uri = URIRef(appellation_namespace[f"forename_{instance.id}"])
            g.add(
                (
                    forename_uri,
                    RDF.type,
                    crm_namespace.E33_E41_Linguistic_Appellation,
                )
            )
            g.add(
                (
                    self.appellation_uri,
                    crm_namespace.P106_is_composed_of,
                    forename_uri,
                )
            )
            g.add((forename_uri, RDFS.label, Literal(instance.forename)))

        if hasattr(instance, "surname"):
            surname_uri = URIRef(appellation_namespace[f"surname_{instance.id}"])
            g.add(
                (
                    surname_uri,
                    RDF.type,
                    crm_namespace.E33_E41_Linguistic_Appellation,
                )
            )
            g.add(
                (
                    self.appellation_uri,
                    crm_namespace.P106_is_composed_of,
                    surname_uri,
                )
            )
            g.add((surname_uri, RDFS.label, Literal(instance.surname)))

        if instance.start_date_written:
            birth_event = URIRef(attributes_namespace[f"birth_{instance.id}"])
            birth_time_span = URIRef(
                attributes_namespace[f"birth_time-span_{instance.id}"]
            )
            g.add((birth_event, RDF.type, crm_namespace.E67_Birth))
            g.add(
                (
                    birth_event,
                    crm_namespace.P98_brought_into_life,
                    self.instance_uri,
                )
            )
            g.add(
                (
                    birth_event,
                    crm_namespace["P4_has_time-span"],
                    birth_time_span,
                )
            )
            g.add((birth_time_span, RDF.type, crm_namespace["E52_Time-Span"]))
            g.add(
                (
                    birth_time_span,
                    crm_namespace.P82a_begin_of_the_begin,
                    Literal(instance.start_date, datatype=XSD.date)
                    if instance.start_date is not None
                    else Literal(instance.start_date_written),
                )
            )
            g.add(
                (
                    birth_time_span,
                    crm_namespace.P82b_end_of_the_end,
                    Literal(instance.start_date, datatype=XSD.date)
                    if instance.start_date is not None
                    else Literal(instance.start_date_written),
                )
            )

        if instance.end_date_written:
            death_event = URIRef(attributes_namespace[f"death_{instance.id}"])
            death_time_span = URIRef(
                attributes_namespace[f"death_time-span_{instance.id}"]
            )
            g.add((death_event, RDF.type, crm_namespace.E69_Death))
            g.add(
                (
                    death_event,
                    crm_namespace.P100_was_death_of,
                    self.instance_uri,
                )
            )
            g.add(
                (
                    death_event,
                    crm_namespace["P4_has_time-span"],
                    death_time_span,
                )
            )
            g.add((death_time_span, RDF.type, crm_namespace["E52_Time-Span"]))
            g.add(
                (
                    death_time_span,
                    crm_namespace.P82a_begin_of_the_begin,
                    Literal(instance.end_date, datatype=XSD.date)
                    if instance.end_date is not None
                    else Literal(instance.end_date_written),
                )
            )
            g.add(
                (
                    death_time_span,
                    crm_namespace.P82b_end_of_the_end,
                    Literal(instance.end_date, datatype=XSD.date)
                    if instance.end_date is not None
                    else Literal(instance.end_date_written),
                )
            )

        return g
