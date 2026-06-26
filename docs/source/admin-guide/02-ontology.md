---
title: Create your ontology
---

The heart and soul of your APIS application is its
`ontology`. It describes `entities` and `relations`.

Given that APIS is based on [Django](https://www.djangoproject.com/),
the file where we describe our entities and relations is the
[models.py](https://docs.djangoproject.com/en/stable/topics/db/models/)
file of your APIS project.

You can use the history plugin to version model
instances, i.e. track changes to all objects of a given model in your
ontology, by having the model inherit from [apis_core.models.VersionMixin][].

# Entities

Entities have to inherit from
[apis_core.apis_entities.models.AbstractEntity][].
Like with any other Django model, you can define [model
fields](https://docs.djangoproject.com/en/stable/ref/models/fields/)
describing the attributes of this entity. A simple person model could
look like this:

``` python
from django.db import models
from apis_core.apis_entities.models import AbstractEntity

class Person(AbstractEntity):
     name = models.CharField(blank=True, default="", max_length=1024)
```

[apis_core.apis_entities.models.AbstractEntity][]
brings some useful functionality to entities but also
inherits from
[apis_core.generic.abc.GenericModel][],
which means that as soon as you define your models and [run
migrations](https://docs.djangoproject.com/en/stable/topics/migrations/),
your models will show up in the APIS web interface in the `Entities` menu in
the top left corner. For every `entity` you define, there will be an overview
page that lists all instances for that `entity` as well as a form for
creating, updating, merging and deleting entities.

![Image showing the APIS Entity menu with one item labeled Persons](img/ontology_entity_menu.png)

# Relations

To use the relations module, you have to add it to your
`INSTALLED_APPS`. The module includes templates that add the relation
listing to templates from other `apis_core` modules, so we recommend to
put the relations module at the top of the apps list:

``` python
INSTALLED_APPS = ["apis_core.relations"] + INSTALLED_APPS
```

Relations have to inherit from
[apis_core.relations.models.Relation][].
You will have to set the attributes `subj_model` and
`obj_model`, which each point to some Django model (can also be a
list of Django models). The Django models can be specified by their
class name or using the natural key of the model
(`APP_NAME.MODEL_CLASS`).

A simple relation between a person and a place could look like this:

``` python
from apis_core.relations.models import Relation

class PersonLivedInPlace(Relation):
     subj_model = Person
     obj_model = "other_app.place" # defining the obj_model using the natural key notation
```

You can define the class methods `name` and
`reverse_name` to provide human-readable strings for your
relation model. They default to the `verbose_name`
(`name`) and the `verbose_name` with the string
` reverse` appended (`reverse_name`).

``` python
from apis_core.relations.models import Relation

class PersonLivedInPlace(Relation):
     subj_model = Person
     obj_model = Place

     @classmethod
     def name(self) -> str:
         return "lived in"

     @classmethod
     def reverse_name(self) -> str:
         return "had inhabitant"
```

Now you can create instances of that relation on your entity pages.
