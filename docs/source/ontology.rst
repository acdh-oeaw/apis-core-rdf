Create your :term:`ontology`
============================

The heart and soul of your APIS application is the :term:`ontology`. It
describes :term:`entities<entity>` and :term:`relations<relation>`.

Given that APIS is based on `Django <https://www.djangoproject.com/>`_, the
file where we describe our entities and relations is the `models.py
<https://docs.djangoproject.com/en/stable/topics/db/models/>`_ file of your APIS
project.

.. note::
   You can use the :ref:`history plugin<History plugin>` to version model
   instances, i.e. track changes to all objects of a given model in your
   ontology, by having the model inherit from :ref:`VersionMixin`.

Entities
^^^^^^^^

Entities have to inherit from
:class:`apis_core.apis_entities.models.AbstractEntity`. Like with any other
Django model, you can define `model fields
<https://docs.djangoproject.com/en/stable/ref/models/fields/>`_ describing the
attributes of this entity. A simple person model could look like this:

.. code-block:: python

   from django.db import models
   from apis_core.apis_entities.models import AbstractEntity

   class Person(AbstractEntity):
        name = models.CharField(blank=True, default="", max_length=1024)


:class:`apis_core.apis_entities.models.AbstractEntity` brings some useful
functionality for Entities, but it also itself inherits from
:class:`apis_core.generic.abc.GenericModel`, which means that as soon as
you define your models and `run
migrations <https://docs.djangoproject.com/en/stable/topics/migrations/>`_ your
models will show up in the APIS webinterface in ``Entities`` menu in the
top left corner.
For every :term:`entity` you defined there will be an overview page that
lists all instances for that :term:`entity`, as well as a form for creating,
updating, merging and deleting entities.

.. image:: img/ontology_entity_menu.png
   :alt: Image showing the APIS Entity menu with one item labelled Persons


Relations
^^^^^^^^^

To use the relations module, you have to add it to your ``INSTALLED_APPS``. The module
ships with templates that add the relation listing to templates from other ``apis_core``
modules, so we recommend to put the Relations module at the top of the apps list:

.. code-block:: python

   INSTALLED_APPS = ["apis_core.relations"] + INSTALLED_APPS

Relations have to inherit from :class:`apis_core.relations.models.Relation`. You will
have to set the attribute `subj_model` and `obj_model` which point
to some Django model (can also be a list of Django models). The Django models can be
specified by their class name or using the natural key of the model
(`"APP_NAME.MODEL_CLASS"`).

A simple Relation between a person and a place could look like this:

.. code-block:: python

   from apis_core.relations.models import Relation

   class PersonLivedInPlace(Relation):
        subj_model = Person
        obj_model = "other_app.place" # defining the obj_model using the natural key notation

You can define the class methods `name` and `reverse_name` to provide human readable
strings for your relation model. They default to the `verbose_name` (`name`) and the
`verbose_name` with the string ` reverse` appended (`reverse_name`).

.. code-block:: python

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

Now you can create instances of that relation on your entity pages.

.. note::
   This new module does not change any code in the existing datamodel or codebase. This
   prevents existing projects that use the legacy Triple or TempTriple implementation
   to break.
