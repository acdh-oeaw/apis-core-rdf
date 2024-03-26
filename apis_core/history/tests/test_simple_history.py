from apis_core.apis_relations.models import Property
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from apis_ontology.models import Person, Place, Profession
from apis_core.apis_relations.models import TempTriple
from datetime import datetime, timedelta


class SimpleHistoryTestCase(TestCase):
    """Test of the simple_history package for the ÖBL usecase.
    This expects the ÖBL ontology to be installed and migrated: https://github.com/acdh-oeaw/apis-instance-oebl-pnp
    """

    def setUp(self):
        prop = Property.objects.create(
            name_forward="geboren in", name_reverse="Geburtsort von"
        )
        prop.subj_class.add(ContentType.objects.get(model="person"))
        prop.obj_class.add(ContentType.objects.get(model="place"))
        Person.objects.create(first_name="John", name="Doe")
        Place.objects.create(
            name="Steyr", _history_date=datetime.now() - timedelta(hours=0, minutes=50)
        )

    def test_history(self):
        """Tests the simple version of attributes changed on a models instance."""
        pers = Person.objects.get(first_name="John")
        pers.first_name = "Jane"
        pers.save()
        self.assertEqual(pers.first_name, "Jane")
        pers_history = pers.history.all()
        assert len(pers_history) == 2
        self.assertEqual("Jane", pers.history.most_recent().first_name)
        self.assertEqual("John", pers.history.earliest().first_name)

    def test_history_through_triples(self):
        """Tests the newly introduced function for retrieving triples for a specific version of a model instance."""
        # first entity
        pers = Person.objects.get(first_name="John")
        # second entity
        place = Place.objects.first()
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
        place2 = Place.objects.create(name="testplace")
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
        pers = Person.objects.get(first_name="John")
        pers.history.latest().set_version_tag("test_tag")
        self.assertEqual(pers.history.latest().version_tag, "test_tag")
        pers_history = pers.history.all()
        self.assertEqual(pers_history.count(), 1)
        self.assertEqual(pers_history[0].version_tag, "test_tag")
        # test with temTriple
        pers2 = Person.objects.create(first_name="Jane", name="Doe")
        place = Place.objects.first()
        TempTriple.objects.create(subj=pers2, prop=Property.objects.first(), obj=place)
        pers2.history.latest().set_version_tag("test_tag")
        self.assertEqual(pers2.history.latest().version_tag, "test_tag")
        triples = pers2.history.earliest().get_triples_for_version()
        self.assertEqual(triples[0].version_tag, "test_tag")
        # test that the same tag is not allowed for two versions
        # Given class inheritance indexes need to be set manually, which is not easily possible with Django-simple-history
        # pers2.start_date_written = "2020-01-01"
        # pers2.save()
        # self.assertEqual(pers2.history.all().count(), 2)
        # pers2.history.earliest().set_version_tag("test_tag")
        # # pers2.history.latest().set_version_tag("test_tag")
        # self.assertRaises(
        #     IntegrityError, pers2.history.latest().set_version_tag, "test_tag"
        # )

    def test_history_delete_entry(self):
        """Tests the deletion of an entry."""
        pers = Person.objects.get(first_name="John")
        pers.delete()
        assert len(Person.history.all()) == 2

    def test_history_merge(self):
        """Tests the merge function of the Place model. This is still expected to fail."""
        pl1 = Place.objects.first()
        pl2 = Place.objects.create(
            name="Test", _history_date=datetime.now() - timedelta(hours=0, minutes=10)
        )
        pl1.merge_with(pl2)
        print("save()")

    def test_m2m_save(self):
        """Test if m2m profession is saved correctly."""
        pers = Person.objects.create(
            first_name="John",
            _history_date=datetime.now() - timedelta(hours=0, minutes=10),
        )
        self.assertEqual(pers.first_name, "John")
        pers_history = pers.history.all()
        assert len(pers_history) == 1
        prof = Profession.objects.create(name="Test")
        pers.profession.add(prof)
        pers.first_name = "Jane"
        pers.save()
        assert len(pers.profession.all()) == 1
        assert len(pers.history.latest().profession.all()) == 1
        assert len(pers.history.earliest().profession.all()) == 0

    def test_history_date(self):
        """Test that history is set correctly when not manually set."""
        pers = Person.objects.all().first()
        pers.first_name = "Jane"
        pers.save()
        assert pers.history.earliest().history_date < pers.history.latest().history_date
