# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

from django.test import TestCase

from apis_core.utils import normalize


class NormalizeTest(TestCase):
    def test_clean_uri(self):
        uri = "https://www.geonames.org/2783029/achensee.html"
        res = "https://sws.geonames.org/2783029/"
        self.assertEqual(normalize.clean_uri(uri), res)
