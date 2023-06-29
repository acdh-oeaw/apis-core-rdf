from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from .models import RootObject, Uri


class ModelTestCase(TestCase):
    def setUp(cls):
        # Set up data for the whole TestCase
        user_type = ContentType.objects.get(app_label="auth", model="user")
        RootObject.objects.create(self_contenttype=user_type, name="foo")
        RootObject.objects.create(self_contenttype=user_type)

    def test_root_object(self):
        rfoo = RootObject.objects.get(name="foo")
        rnone = RootObject.objects.get(name="")
        self.assertEquals(str(rfoo), "foo")
        self.assertEquals(str(rnone), "no name provided")

    def test_uri(self):
        ufoo = Uri.objects.create()
        self.assertEquals(str(ufoo), "None")
