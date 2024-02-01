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
            "kind": "https://www.geonames.org/ontology#P.PPL",
            "lat": "47.5",
            "long": "11.7",
            "name": "Achensee",
            "parent": "https://sws.geonames.org/2782113/",
        }
        # https://www.geonames.org/2783029/achensee.html
        uri = str(testdata / "achensee.rdf")
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(uri)
        self.assertEqual(defintion["model"], "apis_ontology.Place")
        self.assertEqual(achensee, attributes)

    def test_get_definition_from_dict_place_from_dnb(self):
        wien = {"name": "Wien", "lat": "048.208199", "lon": "016.371690"}
        # https://d-nb.info/gnd/4066009-6
        uri = str(testdata / "wien.rdf")
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(uri)
        self.assertEqual(defintion["model"], "apis_ontology.Place")
        self.assertEqual(wien, attributes)

    def test_get_definition_from_dict_person_from_dnb(self):
        pierre = {
            "name": "Ramus,Pierre",
            "profession": "https://d-nb.info/gnd/4053309-8",
            "date_of_birth": "1882-04-15",
            "date_of_death": "1942",
            "place_of_birth": "https://d-nb.info/gnd/4066009-6",
        }
        # https://d-nb.info/gnd/118833197
        uri = str(testdata / "ramus.rdf")
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(uri)
        self.assertEqual(defintion["model"], "apis_ontology.Person")
        self.assertEqual(pierre, attributes)

    def test_get_definition_from_dict_institution_from_dnb(self):
        pierre_ges = {
            "name": "Pierre-Ramus-Gesellschaft",
            "altName": "Pierre Ramus-Gesellschaft",
            "place": "https://d-nb.info/gnd/4066009-6",
        }
        # https://d-nb.info/gnd/415006-5
        uri = str(testdata / "ramus_gesellschaft.rdf")
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(uri)
        self.assertEqual(defintion["model"], "apis_ontology.Institution")
        self.assertEqual(pierre_ges, attributes)

    def test_get_definition_from_dict_institution_from_dnb2(self):
        pierre_ges = {
            "name": "Akademie der Wissenschaften in Wien",
            "altName": "Akademie der Wissenschaften (Wien)",
            "place": "https://d-nb.info/gnd/4066009-6",
            "start_date_written": "1919",
            "end_date_written": "1947",
        }
        # https://d-nb.info/gnd/35077-1
        uri = str(testdata / "oeaw.rdf")
        defintion, attributes = rdf.get_definition_and_attributes_from_uri(uri)
        self.assertEqual(defintion["model"], "apis_ontology.Institution")
        self.assertEqual(pierre_ges, attributes)
