# SPDX-FileCopyrightText: 2023 Birger Schacht
# SPDX-License-Identifier: MIT

from django.test import TestCase

from .helpers import construct_lookup

lookups = {
    "*foo*": ("__icontains", "foo"),
    "foo": ("__icontains", "foo"),
    "*foo": ("__iendswith", "foo"),
    "foo*": ("__istartswith", "foo"),
    '"foo"': ("__iexact", "foo"),
}


class FilterMethodstest(TestCase):
    def test_lookup(self):
        for lookup in lookups:
            self.assertEqual(construct_lookup(lookup), lookups[lookup])
