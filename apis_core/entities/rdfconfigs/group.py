from apis_core.utils.rdf import Attribute, Filter


class E74_GroupFromDNB:
    filter_type_1 = Filter([("rdf:type", "gndo:CorporateBody")])
    filter_type_2 = Filter([("rdf:type", "gndo:Company")])
    filter_type_3 = Filter([("rdf:type", "gndo:FictiveCorporateBody")])
    filter_type_4 = Filter([("rdf:type", "gndo:MusicalCorporateBody")])
    filter_type_5 = Filter([("rdf:type", "gndo:OrganOfCorporateBody")])
    filter_type_6 = Filter([("rdf:type", "gndo:ProjectOrProgram")])
    filter_type_7 = Filter([("rdf:type", "gndo:ReligiousAdministrativeUnit")])
    filter_type_8 = Filter([("rdf:type", "gndo:ReligiousCorporateBody")])

    label = Attribute(
        [
            "gndo:preferredNameForTheCorporateBody",
            "gndo:variantNameForTheCorporateBody",
        ]
    )
    start_date = Attribute("gndo:dateOfEstablishment")
    end_date = Attribute("gndo:dateOfTermination")
    sameas = Attribute("owl:sameAs")


class E74_GroupFromWikidata:
    filter_p31_is_q414147 = Filter([("wdt:P31", "wd:Q414147")])

    label = Attribute(["schema:about/rdfs:label", "rdfs:label"])
    same_as = Attribute(
        ["owl:sameAs", "wdtn:P227", "wdtn:P1566", "wdtn:P214", "wdtn:P244"]
    )
