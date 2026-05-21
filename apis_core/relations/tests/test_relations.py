import pytest
from django.core.exceptions import ValidationError

from apis_core.relations.tests.models import Bar, Baz, Foo, FooBarRelation


@pytest.mark.django_db
class TestRelations(object):
    @pytest.fixture
    def setup(self):
        self.foo = Foo.objects.create()
        self.bar = Bar.objects.create()
        self.baz = Baz.objects.create()

    def test_relation(self, setup):
        """Check if a relation can be created"""
        FooBarRelation(subj=self.foo, obj=self.bar).save()

    def test_relation_wrong_subject(self, setup):
        with pytest.raises(ValidationError, match=r"Baz object \(1\) is not of type"):
            FooBarRelation(subj=self.baz, obj=self.bar).save()

    def test_relation_wrong_object(self, setup):
        with pytest.raises(ValidationError, match=r"Baz object \(1\) is not of type"):
            FooBarRelation(subj=self.foo, obj=self.baz).save()
