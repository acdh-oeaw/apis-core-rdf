from apis_core.utils.rdf import Attribute, Filter


class E21_PersonFromDNB:
    filter_type_is_differentiated_person = Filter(
        [("rdf:type", "gndo:DifferentiatedPerson")]
    )

    forename = Attribute(
        [
            "gndo:preferredNameEntityForThePerson/gndo:forename",
            "gndo:variantNameForThePerson/gndo:forename",
            "gndo:forename",
            "gndo:preferredNameForThePerson",
        ]
    )
    surname = Attribute(
        [
            "gndo:preferredNameEntityForThePerson/gndo:surname",
            "gndo:variantNameForThePerson/gndo:surname",
            "gndo:surname",
        ]
    )
    alternative_names = Attribute("gndo:variantNameForThePerson")
    date_of_birth = Attribute("gndo:dateOfBirth")
    date_of_death = Attribute("gndo:dateOfDeath")
    same_as = Attribute("owl:sameAs")
    profession = Attribute("gndo:professionOrOccupation")


class E21_PersonFromWikidata:
    filter_p31_is_q5 = Filter([("wdt:P31", "wd:Q5")])

    forename = Attribute("wdt:P735/rdfs:label")
    surname = Attribute("wdt:P734/rdfs:label")
    date_of_birth = Attribute("wdt:P569")
    date_of_death = Attribute("wdt:P570")
    same_as = Attribute(
        ["owl:sameAs", "wdtn:P227", "wdtn:P1566", "wdtn:P214", "wdtn:P244"]
    )
