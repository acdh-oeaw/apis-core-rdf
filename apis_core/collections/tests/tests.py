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

    def test_parent_name(self):
        nameparent = fake.name()
        namechild = fake.name()
        parent = SkosCollection.objects.create(name=nameparent)
        child = SkosCollection.objects.create(name=namechild, parent=parent)
        self.assertEqual(str(child.parent), nameparent)
        self.assertEqual(len(parent.children()), 1)

    def test_parent_children(self):
        parent = SkosCollection.objects.create()
        SkosCollection.objects.create(parent=parent)
        self.assertEqual(len(parent.children()), 1)

    def test_parent_children_tree_as_list(self):
        parent = SkosCollection.objects.create()
        child1 = SkosCollection.objects.create(parent=parent)
        child2 = SkosCollection.objects.create(parent=child1)
        self.assertEqual(parent.children_tree_as_list(), [parent, child1, child2])


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
