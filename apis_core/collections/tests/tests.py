from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker

from apis_core.collections.models import SkosCollection, SkosCollectionContentObject

fake = Faker()


class SkosCollectionTestCase(TestCase):
    def test_name(self):
        name = fake.name()
        skc = SkosCollection.objects.create(name=name)
        self.assertEqual(str(skc), name)


class SkosCollectionContentObjectTestCase(TestCase):
    def setUp(self):
        self.collection_name = fake.color_name()
        self.collection = SkosCollection.objects.create(name=self.collection_name)

    def test_collection(self):
        user = User.objects.create(username=fake.name())
        scco = SkosCollectionContentObject(
            collection=self.collection, content_object=user
        )
        self.assertEqual(str(scco), f"{user} -> {self.collection_name}")
