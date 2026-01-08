class E21_PersonFromDNB:
    filters = [{"rdf:type": "gndo:DifferentiatedPerson"}]

    class Attributes:
        forename = [
            "gndo:preferredNameEntityForThePerson/gndo:forename",
            "gndo:variantNameForThePerson/gndo:forename",
            "gndo:forename",
            "gndo:preferredNameForThePerson",
        ]
        surname = [
            "gndo:preferredNameEntityForThePerson/gndo:surname",
            "gndo:variantNameForThePerson/gndo:surname",
            "gndo:surname",
        ]
        alternative_names = "gndo:variantNameForThePerson"
        date_of_birth = "gndo:dateOfBirth"
        date_of_death = "gndo:dateOfDeath"
        same_as = "owl:sameAs"
        profession = "gndo:professionOrOccupation"


class E21_PersonFromWikidata:
    filters = [{"wdt:P31": "wd:Q5"}]

    class Attributes:
        forename = "wdt:P735/rdfs:label"
        surname = "wdt:P734/rdfs:label"
        date_of_birth = "wdt:P569"
        date_of_death = "wdt:P570"
        same_as = ["owl:sameAs", "wdtn:P227", "wdtn:P1566", "wdtn:P214", "wdtn:P244"]
