from django.db import models

from apis_core.relations.models import Relation


class Foo(models.Model): ...


class Bar(models.Model): ...


class Baz(models.Model): ...


class FooBarRelation(Relation):
    subj_model = Foo
    obj_model = Bar
