class E74_GroupFromDNB:
    filters = [
        {"rdf:type": "gndo:CorporateBody"},
        {"rdf:type": "gndo:Company"},
        {"rdf:type": "gndo:FictiveCorporateBody"},
        {"rdf:type": "gndo:MusicalCorporateBody"},
        {"rdf:type": "gndo:OrganOfCorporateBody"},
        {"rdf:type": "gndo:ProjectOrProgram"},
        {"rdf:type": "gndo:ReligiousAdministrativeUnit"},
        {"rdf:type": "gndo:ReligiousCorporateBody"},
    ]

    class Attributes:
        label = [
            "gndo:preferredNameForTheCorporateBody",
            "gndo:variantNameForTheCorporateBody",
        ]
        start_date = "gndo:dateOfEstablishment"
        end_date = "gndo:dateOfTermination"
        sameas = "owl:sameAs"


class E74_GroupFromWikidata:
    filters = [{"wdt:P31": "wd:Q414147"}]

    class Attributes:
        label = ["schema:about/rdfs:label", "rdfs:label"]
        same_as = ["owl:sameAs", "wdtn:P227", "wdtn:P1566", "wdtn:P214", "wdtn:P244"]
