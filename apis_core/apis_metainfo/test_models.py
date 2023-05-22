from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from .models import RootObject, Source, Uri


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
        s = Source.objects.create()
        s_fname = Source.objects.create(orig_filename="file_name_of_source")
        s_fname_aut = Source.objects.create(
            orig_filename="file_name_of_source", author="Alice"
        )
        self.assertEquals(str(s), f"(ID: {s.id})")
        self.assertEquals(str(s_fname), "file_name_of_source")
        self.assertEquals(
            str(s_fname_aut),
            "file_name_of_source, stored by Alice",
        )

    def test_uri(self):
        ufoo = Uri.objects.create()
        self.assertEquals(str(ufoo), "None")
