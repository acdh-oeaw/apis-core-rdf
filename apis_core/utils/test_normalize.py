# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

from django.test import TestCase

from apis_core.utils import normalize


class NormalizeTest(TestCase):
    def test_clean_uri_geonames(self):
        uri = "https://www.geonames.org/2783029/achensee.html"
        res = "https://sws.geonames.org/2783029/"
        self.assertEqual(normalize.clean_uri(uri), res)

    def test_clean_uri_wikidata(self):
        uri = "https://www.wikidata.org/wiki/Q1735"
        res = "http://www.wikidata.org/entity/Q1735"
        self.assertEqual(normalize.clean_uri(uri), res)

    def test_clean_uri_dnb(self):
        uri = "https://d-nb.info/gnd/118540475"
        res = "https://d-nb.info/gnd/118540475"
        self.assertEqual(normalize.clean_uri(uri), res)
