import time
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
        prop = Property.objects.create(name="geboren in")
        prop.subj_class.add(ContentType.objects.get(model="person"))
        prop.obj_class.add(ContentType.objects.get(model="place"))
        Person.objects.create(first_name="John", name="Doe")
        place = Place.objects.create(
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
        pers = Person.objects.get(first_name="John")
        place = Place.objects.first()
        place.name = "Ennsleite"
        place.save()
        TempTriple.objects.create(subj=pers, prop=Property.objects.first(), obj=place)
        assert len(Place.history.earliest().get_triples_for_version()) == 0
        assert len(Place.history.latest().get_triples_for_version()) == 1
        triples = Place.history.latest().get_triples_for_version()
        print("fin")

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
