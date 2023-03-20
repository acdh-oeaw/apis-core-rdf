from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from .models import RootObject, Source, Uri, UriCandidate


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

    def test_source(self):
        sfoo = Source.objects.create(author="foo", orig_filename="bar")
        snone = Source.objects.create()
        self.assertEquals(str(sfoo), "bar, stored by foo")
        self.assertEquals(str(snone), f"(ID: {snone.id})")

    def test_uri(self):
        ufoo = Uri.objects.create()
        self.assertEquals(str(ufoo), "None")

    def test_uri_candidate(self):
        ufoo = UriCandidate.objects.create()
        self.assertEquals(str(ufoo), "UriCandidate object (1)")
