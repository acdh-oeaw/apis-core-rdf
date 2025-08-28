import pytest
from django.contrib.contenttypes.models import ContentType
from faker import Faker
from pytest_django.asserts import assertContains, assertTemplateUsed

from apis_core.uris.models import Uri
from apis_core.uris.tests.models import Dummy, Person

fake = Faker()


@pytest.mark.django_db
class TestUris(object):
    @pytest.fixture
    def setup(self):
        # Create a couple of person objects
        for _ in range(0, fake.random_int(5, 20)):
            Person.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name()
            )

    def test_uris_count(self, setup):
        """Check if the correct number of Uris was created"""
        assert Uri.objects.count() == Person.objects.count()

    def test_uris_list_view_status(self, setup, admin_client):
        """Check if the uris list view works"""
        response = admin_client.get("/uris.uri/")
        assert response.status_code == 200

    def test_uris_list_view_content(self, setup, admin_client):
        """Check if the uris list view works"""
        response = admin_client.get("/uris.uri/")
        count = Person.objects.count()
        # check for the correct result count in the response content
        assertContains(response, f"{count} results.")
        # check if all the persons are listed
        for p in Person.objects.all():
            assertContains(response, str(p))

    def test_delete_view_template_override(self, setup, admin_client):
        """Check that the delete confirm view uses the right template"""
        response = admin_client.get("/uris.uri/delete/1")
        uri = Uri.objects.get(pk=1)
        assertTemplateUsed(response, "uris/uri_confirm_delete.html")
        assertContains(response, uri.uri)
        assertContains(response, str(uri.content_object))

    def test_no_uris_for_dummy(self):
        """Check that we don't create uris for dummy objects"""
        for _ in range(0, 5):
            Dummy.objects.create()
        content_type = ContentType.objects.get_for_model(Dummy)
        assert Uri.objects.filter(content_type=content_type).count() == 0

    def test_custom_uri(self):
        d = Dummy.objects.create()
        uri = "http://example.org"
        d._uris = [uri]
        d.save()
        assert Uri.objects.filter(uri=uri).exists()
        assert Uri.objects.get(uri=uri).content_object == d
