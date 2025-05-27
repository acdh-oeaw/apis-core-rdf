# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

from pathlib import Path

from django.test import TestCase

from apis_core.utils import rdf

# use `curl -H "Accept: application/rdf+xml" -L $URI` to fetch data

testdata = Path(__file__).parent / "testdata"


class RdfTest(TestCase):
    def test_get_definition_from_dict_place_from_geonames(self):
        achensee = {
            "latitude": ["47.5"],
            "longitude": ["11.7"],
            "label": ["Achensee"],
        }
        # https://www.geonames.org/2783029/achensee.html
        uri = str(testdata / "achensee.rdf")

        attributes = rdf.get_something_from_uri(uri)
        self.assertEqual(achensee["latitude"], attributes["latitude"])
        self.assertEqual(achensee["longitude"], attributes["longitude"])
        self.assertEqual(achensee["label"], attributes["label"])

    def test_get_definition_from_dict_place_from_dnb(self):
        wien = {
            "label": ["Wien"],
            "latitude": ["+048.208199"],
            "longitude": ["016.371690"],
        }
        # https://d-nb.info/gnd/4066009-6
        uri = str(testdata / "wien.rdf")

        attributes = rdf.get_something_from_uri(uri)
        self.assertEqual(wien["latitude"], attributes["latitude"])
        self.assertEqual(wien["longitude"], attributes["longitude"])
        self.assertEqual(wien["label"], attributes["label"])

    def test_get_definition_from_dict_person_from_dnb(self):
        pierre = {
            "forename": [
                "Pierre",
                "Pʹer",
                "Rudolf",
                "Rodolphe",
                "...",
            ],
            "surname": ["Ramus", "Großmann", "Grossmann", "Grossman", "Libertarian"],
            "alternative_names": [
                "Ramus, Pʹer",
                "Großmann, Rudolf",
                "Grossmann, Rudolf",
                "Grossman, Rudolf",
                "Grossman, Rodolphe",
                "Grossmann, Rodolphe",
                "Libertarian, ...",
            ],
            "date_of_birth": ["1882-04-15"],
            "date_of_death": ["1942"],
        }
        # https://d-nb.info/gnd/118833197
        uri = str(testdata / "ramus.rdf")

        attributes = rdf.get_something_from_uri(uri)
        self.assertEqual(pierre["forename"], attributes["forename"])
        self.assertEqual(pierre["surname"], attributes["surname"])
        # self.assertEqual(pierre["alternative_names"], attributes["alternative_names"])
        self.assertEqual(pierre["date_of_birth"], attributes["date_of_birth"])
        self.assertEqual(pierre["date_of_death"], attributes["date_of_death"])

    def test_get_definition_from_dict_institution_from_dnb(self):
        pierre_ges = {
            "label": [
                "Pierre-Ramus-Gesellschaft",
                "Ramus-Gesellschaft",
                "Pierre Ramus-Gesellschaft",
            ],
        }
        # https://d-nb.info/gnd/415006-5
        uri = str(testdata / "ramus_gesellschaft.rdf")

        attributes = rdf.get_something_from_uri(uri)
        self.assertEqual(pierre_ges["label"], attributes["label"])

    def test_get_definition_from_dict_institution_from_dnb2(self):
        oeaw = {
            "label": [
                "Akademie der Wissenschaften in Wien",
                "Academy of Sciences in Vienna",
                "Akademie der Wissenschaften (Wien)",
            ],
        }
        # https://d-nb.info/gnd/35077-1
        uri = str(testdata / "oeaw.rdf")

        attributes = rdf.get_something_from_uri(uri)
        self.assertEqual(oeaw["label"], attributes["label"])
