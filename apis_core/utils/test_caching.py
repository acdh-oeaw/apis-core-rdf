from django.test import TestCase

from apis_core.utils import caching

all_class_modules_and_names = {
    "apis_metainfo": [
        "RootObject",
        "Uri",
    ],
    "apis_relations": [
        "TempTriple",
        "Property",
        "Triple",
        "VersionTempTriple",
    ],
    "contenttypes": ["ContentType"],
}


class CachingTest(TestCase):
    def test_get_all_class_modules_and_names(self):
        expected = []
        for key in all_class_modules_and_names:
            for name in all_class_modules_and_names[key]:
                expected.append((key, name))
        res = caching.get_all_class_modules_and_names()
        self.assertEqual(res, expected)
