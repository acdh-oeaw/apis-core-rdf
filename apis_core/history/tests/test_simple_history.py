from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from apis_core.apis_relations.models import Property, TempTriple
from sample_project.models import Person, Place, Profession


class SimpleHistoryTestCase(TestCase):
    """Test of the simple_history package using the demo project"""

    def setUp(self):
        self.Person = Person
        self.Place = Place
        self.Profession = Profession

        prop = Property.objects.create(
            name_forward="geboren in", name_reverse="Geburtsort von"
        )
        prop.subj_class.add(ContentType.objects.get(model="person"))
        prop.obj_class.add(ContentType.objects.get(model="place"))
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

    def test_history_through_triples(self):
        """Tests the newly introduced function for retrieving triples for a specific version of a model instance."""
        # first entity
        pers = self.Person.objects.get(forename="John")
        # second entity
        place = self.Place.objects.first()
        # create a triple
        tt1 = TempTriple.objects.create(
            subj=pers, prop=Property.objects.first(), obj=place
        )
        # test that we get one triple version for both entities
        self.assertEqual(len(pers.history.earliest().get_triples_for_version()), 1)
        self.assertEqual(len(place.history.earliest().get_triples_for_version()), 1)
        # change the triple and test again
        tt1.start_date_written = "2020-01-01"
        tt1.save()
        triples = pers.history.earliest().get_triples_for_version()
        self.assertEqual(len(triples), 1)
        self.assertEqual(triples[0].start_date_written, "2020-01-01")
        # change the place and test again
        place2 = self.Place.objects.create(label="testplace")
        tt1.obj = place2
        tt1.save()
        triples = place.history.earliest().get_triples_for_version()
        self.assertEqual(len(triples), 1)
        self.assertEqual(triples[0].obj, place)
        triples = place2.history.earliest().get_triples_for_version()
        self.assertEqual(len(triples), 1)
        self.assertEqual(triples[0].obj, place2)
        # given that the function should return the latest version of a triple, we should get the new place
        triples = pers.history.earliest().get_triples_for_version()
        self.assertEqual(len(triples), 1)
        self.assertEqual(triples[0].obj, place2)
        # test retrieving triples for a specific datetime
        triples = pers.history.earliest().get_triples_for_version(
            history_date=datetime.now() - timedelta(hours=0, minutes=40)
        )
        self.assertEqual(len(triples), 0)

    def test_history_tag(self):
        """Tests the version tag function."""
        pers = self.Person.objects.get(forename="John")
        pers.history.latest().set_version_tag("test_tag")
        self.assertEqual(pers.history.latest().version_tag, "test_tag")
        pers_history = pers.history.all()
        self.assertEqual(pers_history.count(), 1)
        self.assertEqual(pers_history[0].version_tag, "test_tag")
        # test with TemTriple
        pers2 = self.Person.objects.create(forename="Jane", surname="Doe")
        place = self.Place.objects.first()
        TempTriple.objects.create(subj=pers2, prop=Property.objects.first(), obj=place)
        pers2.history.latest().set_version_tag("test_tag")
        self.assertEqual(pers2.history.latest().version_tag, "test_tag")
        triples = pers2.history.earliest().get_triples_for_version()
        self.assertEqual(triples[0].version_tag, "test_tag")

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
