from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from .models import RootObject, Uri


class ModelTestCase(TestCase):
    def setUp(cls):
        # Set up data for the whole TestCase
        user_type = ContentType.objects.get(app_label="auth", model="user")
        RootObject.objects.create(self_contenttype=user_type)

    def test_uri(self):
        ufoo = Uri.objects.create()
        self.assertEqual(str(ufoo), "None")
