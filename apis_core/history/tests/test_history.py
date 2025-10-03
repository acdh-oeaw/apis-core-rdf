from datetime import datetime

import pytest
from faker import Faker

from apis_core.history.tests.models import (
    Person,
    PersonPlaceRelation,
    Place,
    Profession,
)

fake = Faker()


@pytest.mark.django_db
class TestHistory(object):
    def test_history_date_setter(self):
        """Test the date setter of the VersionMixin."""
        person = Person.objects.create()
        person._history_date = datetime(1970, 1, 1, 0, 0).astimezone()
        person.save()
        assert (
            person.history.last().history_date
            == datetime(1970, 1, 1, 0, 0).astimezone()
        )

    def test_history(self):
        """Tests the simple version of attributes changed on a models instance."""
        first_name = fake.first_name()
        last_name = fake.last_name()
        person = Person.objects.create(first_name=first_name, last_name=last_name)
        new_first_name = fake.first_name()
        person.first_name = new_first_name
        person.save()
        assert person.first_name == new_first_name
        person_history = person.history.all()
        assert len(person_history) == 2
        assert person.history.most_recent().first_name == new_first_name
        assert person.history.earliest().first_name == first_name

    def test_history_delete_entry(self):
        """Tests the deletion of an entry."""
        person = Person.objects.create()
        person.delete()
        assert len(Person.history.all()) == 2

    def test_m2m_save(self):
        """Test if m2m profession is saved correctly."""
        person = Person.objects.create()
        person_history = person.history.all()
        assert len(person_history) == 1
        profession = Profession.objects.create(label=fake.job())
        person.profession.add(profession)
        person.save()
        assert len(person.profession.all()) == 1
        assert len(person.history.latest().profession.all()) == 1
        assert len(person.history.earliest().profession.all()) == 0

    def test_history_date(self):
        """Test that history is set correctly when not manually set."""
        person = Person.objects.create()
        person.first_name = fake.first_name()
        person.save()
        assert (
            person.history.earliest().history_date
            < person.history.latest().history_date
        )

    def test_relation_list(self):
        person = Person.objects.create()
        place = Place.objects.create()
        assert len(person.get_history_data()) == 1
        ppr = PersonPlaceRelation.objects.create_between_instances(person, place)
        assert len(person.get_history_data()) == 2
        place = Place.objects.create()
        ppr.obj = place
        ppr.save()
        assert len(person.get_history_data()) == 3
