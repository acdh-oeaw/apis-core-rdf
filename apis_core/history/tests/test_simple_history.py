from datetime import datetime, timedelta

from django.test import TestCase

from sample_project.models import Person, Place, Profession


class SimpleHistoryTestCase(TestCase):
    """Test of the simple_history package using the demo project"""

    def setUp(self):
        self.Person = Person
        self.Place = Place
        self.Profession = Profession

        Person.objects.create(forename="John", surname="Doe")
        Place.objects.create(
            label="Steyr", _history_date=datetime.now() - timedelta(hours=0, minutes=50)
        )

    def test_history(self):
        """Tests the simple version of attributes changed on a models instance."""
        pers = self.Person.objects.get(forename="John")
        pers.forename = "Jane"
        pers.save()
        self.assertEqual(pers.forename, "Jane")
        pers_history = pers.history.all()
        assert len(pers_history) == 2
        self.assertEqual("Jane", pers.history.most_recent().forename)
        self.assertEqual("John", pers.history.earliest().forename)

    def test_history_delete_entry(self):
        """Tests the deletion of an entry."""
        pers = self.Person.objects.get(forename="John")
        pers.delete()
        assert len(self.Person.history.all()) == 2

    def test_history_merge(self):
        """Tests the merge function of the Place model. This is still expected to fail."""
        pl1 = self.Place.objects.first()
        pl2 = self.Place.objects.create(
            label="Test", _history_date=datetime.now() - timedelta(hours=0, minutes=10)
        )
        pl1.merge_with([pl2])
        print("save()")

    def test_m2m_save(self):
        """Test if m2m profession is saved correctly."""
        pers = self.Person.objects.create(
            forename="John",
            _history_date=datetime.now() - timedelta(hours=0, minutes=10),
        )
        self.assertEqual(pers.forename, "John")
        pers_history = pers.history.all()
        assert len(pers_history) == 1
        prof = self.Profession.objects.create(name="Test")
        pers.profession.add(prof)
        pers.forename = "Jane"
        pers.save()
        assert len(pers.profession.all()) == 1
        assert len(pers.history.latest().profession.all()) == 1
        assert len(pers.history.earliest().profession.all()) == 0

    def test_history_date(self):
        """Test that history is set correctly when not manually set."""
        pers = self.Person.objects.all().first()
        pers.forename = "Jane"
        pers.save()
        assert pers.history.earliest().history_date < pers.history.latest().history_date
