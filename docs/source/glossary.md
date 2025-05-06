---
title: Glossary
---

entity

:   An entity is a thing or object that is identifiable and distinct
    from other things. In the context of APIS, an entity is a Django
    data model instance.

property

:   An attribute of an entity. In the context of APIS, a property is a
    field of a Django data model.

TEI

:   [Text encoding Initiative](https://tei-c.org/) is a consortium which
    collectively develops and maintains a standard for the
    representation of texts in digital form. In the context of APIS, TEI
    refers to the XML schema used for the representation of texts.

RDF

:   [Resource Description Framework](https://www.w3.org/RDF/) is a
    standard model for data interchange on the web. In the context of
    APIS, RDF is used to provide data in a machine-readable format via
    the API.

relation

:   A relation is a connection between two entities. In the context of
    APIS, this is realized via the
    [apis_core.relations.models.Relation][] class.

ontology

:   An ontology is a formal representation of knowledge as a set of
    concepts within a domain, and the relationships between those
    concepts. In the context of APIS it is a specialized form of a
    Django data model and therefore refers to classes rather than
    instances.
