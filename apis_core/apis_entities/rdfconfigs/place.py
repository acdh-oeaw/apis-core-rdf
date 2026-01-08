from apis_core.utils.rdf import Attribute, Filter


class PlaceFromDNB:
    filter_type_is_naturalgeographicunit = Filter(
        [("rdf:type", "gndo:NaturalGeographicUnit")]
    )
    filter_type_is_tcb_or_adu = Filter(
        [("rdf:type", "gndo:TerritorialCorporateBodyOrAdministrativeUnit")]
    )

    label = Attribute("gndo:preferredNameForThePlaceOrGeographicName")
    longitude = Attribute("""
    SELECT ?longitude
    WHERE {
      ?subject geo:hasGeometry/geo:asWKT ?point .
      BIND(REPLACE(str(?point), "Point \\( \\+?(-?\\d+.\\d+).*", "$1") as ?longitude)
    }
    """)
    latitude = Attribute("""
    SELECT ?latitude
    WHERE {
      ?subject geo:hasGeometry/geo:asWKT ?point .
      BIND(REPLACE(str(?point), "^Point\\s*\\(\\s*[+-]?\\d+\\.\\d+\\s+([+-]?\\d+\\.\\d+)\\s*\\)$", "$1") as ?latitude)
    }
    """)
    same_as = Attribute("owl:sameAs")


class PlaceFromGeonames:
    filter_type_is_feature = Filter([("rdf:type", "gn:Feature")])

    label = Attribute(["gn:name", "gn:officialName", "gn:alternateName"])
    latitude = Attribute("wgs84_pos:lat")
    longitude = Attribute("wgs84_pos:long")
    same_as = Attribute(["rdfs:seeAlso", "gn:wikipediaArticle"])


class PlaceFromWikidata:
    filter_p625_must_exist = Filter([("wdt:P625", True)])

    label = Attribute(
        [
            "rdfs:label,de",
            "rdfs:label,en",
            "wdt:P1448/rdfs:label",
            "rdfs:label",
        ]
    )
    longitude = Attribute("""
    SELECT ?longitude
    WHERE {
      ?subject wdt:P625 ?geo1 .
      BIND(REPLACE(str(?geo1), "Point\\(([-+]?\\d+\\.?\\d+).*$", "$1") as ?longitude)
      }
    """)
    latitude = Attribute("""
    SELECT ?latitude
    WHERE {
      ?subject wdt:P625 ?geo1 .
      BIND(REPLACE(str(?geo1), "Point\\(([-+]?\\d+\\.?\\d+) ([-+]?\\d+\\.?\\d+).*$", "$2") as ?latitude)
      }
    """)
    same_as = Attribute(
        ["owl:sameAs", "wdtn:P227", "wdtn:P1566", "wdtn:P214", "wdtn:P244"]
    )
