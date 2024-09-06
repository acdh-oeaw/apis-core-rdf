# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

from pathlib import Path

from django.test import TestCase

from apis_core.apis_entities.abc import E21_Person, E53_Place, E74_Group
from apis_core.utils import rdf

# use `curl -H "Accept: application/rdf+xml" -L $URI` to fetch data

testdata = Path(__file__).parent / "testdata"


class Place(E53_Place):
    class Meta:
        app_label = "test"


class Person(E21_Person):
    class Meta:
        app_label = "test"


class Institution(E74_Group):
    class Meta:
        app_label = "test"


class RdfTest(TestCase):
    def test_get_definition_from_dict_place_from_geonames(self):
        achensee = {
            "latitude": "47.5",
            "longitude": "11.7",
            "label": "Achensee",
        }
        # https://www.geonames.org/2783029/achensee.html
        uri = str(testdata / "achensee.rdf")

        place = Place()
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(uri, place)
        self.assertEqual(achensee, attributes)

    def test_get_definition_from_dict_place_from_dnb(self):
        wien = {"label": "Wien", "latitude": "048.208199", "longitude": "016.371690"}
        # https://d-nb.info/gnd/4066009-6
        uri = str(testdata / "wien.rdf")

        place = Place()
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(uri, place)
        self.assertEqual(wien, attributes)

    def test_get_definition_from_dict_person_from_dnb(self):
        pierre = {
            "forename": "Pierre",
            "surname": "Ramus",
            "date_of_birth": "1882-04-15",
            "date_of_death": "1942",
        }
        # https://d-nb.info/gnd/118833197
        uri = str(testdata / "ramus.rdf")

        person = Person()
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(uri, person)
        self.assertEqual(pierre, attributes)

    def test_get_definition_from_dict_institution_from_dnb(self):
        pierre_ges = {
            "label": "Pierre-Ramus-Gesellschaft",
        }
        # https://d-nb.info/gnd/415006-5
        uri = str(testdata / "ramus_gesellschaft.rdf")

        institution = Institution()
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(
            uri, institution
        )
        self.assertEqual(pierre_ges, attributes)

    def test_get_definition_from_dict_institution_from_dnb2(self):
        pierre_ges = {
            "label": "Akademie der Wissenschaften in Wien",
        }
        # https://d-nb.info/gnd/35077-1
        uri = str(testdata / "oeaw.rdf")

        institution = Institution()
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(
            uri, institution
        )
        self.assertEqual(pierre_ges, attributes)
