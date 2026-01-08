class PlaceFromDNB:
    filters = [
        {"rdf:type": "gndo:NaturalGeographicUnit"},
        {"rdf:type": "gndo:TerritorialCorporateBodyOrAdministrativeUnit"},
    ]

    class Attributes:
        label = "gndo:preferredNameForThePlaceOrGeographicName"
        longitude = """
        SELECT ?longitude
        WHERE {
          ?subject geo:hasGeometry/geo:asWKT ?point .
          BIND(REPLACE(str(?point), "Point \\( \\+?(-?\\d+.\\d+).*", "$1") as ?longitude)
        }
        """
        latitude = """
        SELECT ?latitude
        WHERE {
          ?subject geo:hasGeometry/geo:asWKT ?point .
          BIND(REPLACE(str(?point), "^Point\\s*\\(\\s*[+-]?\\d+\\.\\d+\\s+([+-]?\\d+\\.\\d+)\\s*\\)$", "$1") as ?latitude)
        }
        """
        same_as = "owl:sameAs"


class PlaceFromGeonames:
    filters = [{"rdf:type": "gn:Feature"}]

    class Attributes:
        label = ["gn:name", "gn:officialName", "gn:alternateName"]
        latitude = "wgs84_pos:lat"
        longitude = "wgs84_pos:long"
        same_as = ["rdfs:seeAlso", "gn:wikipediaArticle"]


class PlaceFromWikidata:
    filters = [{"wdt:P625": True}]

    class Attributes:
        label = [
            "rdfs:label,de",
            "rdfs:label,en",
            "wdt:P1448/rdfs:label",
            "rdfs:label",
        ]
        longitude = """
        SELECT ?longitude
        WHERE {
          ?subject wdt:P625 ?geo1 .
          BIND(REPLACE(str(?geo1), "Point\\(([-+]?\\d+\\.?\\d+).*$", "$1") as ?longitude)
          }
        """
        latitude = """
        SELECT ?latitude
        WHERE {
          ?subject wdt:P625 ?geo1 .
          BIND(REPLACE(str(?geo1), "Point\\(([-+]?\\d+\\.?\\d+) ([-+]?\\d+\\.?\\d+).*$", "$2") as ?latitude)
          }
        """
        same_as = ["owl:sameAs", "wdtn:P227", "wdtn:P1566", "wdtn:P214", "wdtn:P244"]
