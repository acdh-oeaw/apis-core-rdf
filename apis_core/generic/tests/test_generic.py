import pytest
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from faker import Faker
from pytest_django.asserts import assertContains

from apis_core.generic.tests.models import Dummy, Person
from apis_core.generic.tests.tables import DummyTable
from apis_core.generic.views import List

fake = Faker()

# tuple of route, permission, and expected status_code
routes = [
    ("/generic_tests.person/", "view_person", 200),
    ("/generic_tests.person/1", "view_person", 200),
    ("/generic_tests.person/create", "add_person", 200),
    ("/generic_tests.person/delete/1", "delete_person", 200),
    ("/generic_tests.person/update/1", "change_person", 200),
    ("/generic_tests.person/duplicate/1", "add_person", 302),
    ("/generic_tests.person/autocomplete", "view_person", 200),
    ("/generic_tests.person/import", "add_person", 200),
    ("/generic_tests.person/selectmergeorenrich/1", "add_person", 200),
    ("/generic_tests.person/merge/1/2", "change_person", 200),
    (
        "/generic_tests.person/enrich/1?uri=https://d-nb.info/gnd/119252880",
        "change_person",
        200,
    ),
]
route_parameters = "route,permission,status_code"

unique_first_name = "SomeUniqueFirstName"
unique_last_name = "SomeUniqueLastName"


@pytest.mark.django_db
class TestGeneric(object):
    @pytest.fixture
    def setup(self):
        # Create an admin user
        self.admin = User.objects.create_superuser(
            "admin", fake.email(), fake.password()
        )
        # Create a normal user
        self.user = User.objects.create_user(
            fake.user_name(), fake.email(), fake.password()
        )
        # Create a couple of person objects
        for _ in range(0, fake.random_int(5, 20)):
            Person.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name()
            )
        self.unique = Person.objects.create(
            first_name=unique_first_name, last_name=unique_last_name
        )
        # Create a person without any attributes
        Person.objects.create()
        self.person_count = Person.objects.count()

    def test_person_count(self, setup):
        """Check if the correct number of persons was created"""
        assert Person.objects.count() == self.person_count

    # Initial tests for checking the permissions of the views

    @pytest.mark.parametrize(route_parameters, routes)
    def test_anon_person_views(self, setup, route, permission, status_code, client):
        """Anon user should not be able to access the person views"""
        response = client.get(route)
        assert response.status_code == 302

    @pytest.mark.parametrize(route_parameters, routes)
    def test_admin_person_views(
        self, setup, route, permission, status_code, admin_client
    ):
        """Admin user should be able to access the person list"""
        response = admin_client.get(route)
        assert response.status_code == status_code

    @pytest.mark.parametrize(route_parameters, routes)
    def test_person_user_views(self, setup, route, permission, status_code, client):
        """Normal user should not be able to access the person list"""
        client.force_login(self.user)
        response = client.get(route)
        assert response.status_code == 403

    @pytest.mark.parametrize(route_parameters, routes)
    def test_person_user_with_access(
        self, setup, route, permission, status_code, client
    ):
        """Normal user should be able to access the person views after bein granted permission"""
        content_type = ContentType.objects.get_for_model(Person)
        p = Permission.objects.get(codename=permission, content_type=content_type)
        self.user.user_permissions.add(p)
        client.force_login(self.user)
        response = client.get(route)
        assert response.status_code == status_code

    # More detailed tests checking the content of the responses and sending actual data

    def test_person_list(self, setup, admin_client):
        """Check if the first_name of some person object is listed in the person list"""
        p = Person.objects.order_by("?").first()
        response = admin_client.get("/generic_tests.person/")
        assert p.first_name in response.content.decode()

    def test_person_detail(self, setup, admin_client):
        """Check if the details page of a person lists its details"""
        p = Person.objects.order_by("?").first()
        response = admin_client.get(f"/generic_tests.person/{p.pk}")
        assert p.first_name in response.content.decode()
        assert p.last_name in response.content.decode()

    def test_person_create(self, setup, admin_client):
        """Check if we can create a person using the create route"""
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        response = admin_client.post("/generic_tests.person/create", data, follow=True)
        assert response.status_code == 200
        assert data["first_name"] in response.content.decode()
        assert data["last_name"] in response.content.decode()
        assert Person.objects.count() == self.person_count + 1

    def test_person_delete(self, setup, admin_client):
        """Check if we can delete a person using the delete route"""
        p = Person.objects.order_by("?").first()
        response = admin_client.get(f"/generic_tests.person/delete/{p.pk}")
        assert response.status_code == 200
        assert "Confirm deletion of:" in response.content.decode()
        assert str(p) in response.content.decode()

    def test_person_delete_confirmation(self, setup, admin_client):
        """Check if we can delete a person using the delete route"""
        p = self.unique
        response = admin_client.post(
            f"/generic_tests.person/delete/{p.pk}", follow=True
        )
        assert response.status_code == 200
        assert p.first_name not in response.content.decode()
        assert p.last_name not in response.content.decode()
        assert Person.objects.count() == self.person_count - 1

    def test_person_delete_redirect(self, setup, admin_client):
        """Check if we can delete a person using the delete route"""
        p = self.unique
        response = admin_client.post(
            f"/generic_tests.person/delete/{p.pk}?redirect=/generic_tests.person/create"
        )
        assert response.status_code == 302
        assert response.headers["Location"] == "/generic_tests.person/create"

    def test_person_update(self, setup, admin_client):
        """Check if we can update a person"""
        p = Person.objects.order_by("?").first()
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        response = admin_client.post(
            f"/generic_tests.person/update/{p.pk}", data, follow=True
        )
        assert response.status_code == 200
        assert Person.objects.get(pk=p.pk).last_name == data["last_name"]
        assert Person.objects.get(pk=p.pk).first_name == data["first_name"]

    def test_person_autocomplete(self, setup, admin_client):
        """Check if we find a person using autocomplete"""
        p = self.unique
        response = admin_client.get(
            f"/generic_tests.person/autocomplete?q={p.first_name}"
        )
        assert response.status_code == 200
        expected = {
            "results": [{"id": str(p.pk), "selected_text": str(p), "text": str(p)}],
            "pagination": {"more": False},
        }
        assert response.json() == expected

    def test_person_table_export_filename(self, rf, admin_user):
        """Check if the person table provides the correct export filename"""
        view = List(model=Person)
        assert view.get_export_filename("ext") == "table.ext"

    def test_dummy_table_export_filename(self, rf, admin_user):
        """Check if the dummy table provides the correct export filename"""
        view = List(model=Dummy)
        assert view.get_export_filename("ext") == "dummytable.ext"

    def test_dummy_table_class(self, admin_client):
        request = admin_client.get("/generic_tests.dummy/")
        assert isinstance(request.context["table"], DummyTable)

    def test_list_view_contains_columns(self, admin_client):
        """Check if the columns selector is present & if some of the options are present"""
        response = admin_client.get("/generic_tests.person/")
        assertContains(
            response,
            '<select name="columns" class="selectmultiple form-select" id="id_columns" multiple>',
        )
        assertContains(response, '<option value="id" selected>ID</option>')
        assertContains(response, '<option value="first_name">First name</option>')
        assertContains(response, '<option value="last_name">Last name</option>')
