Create your :term:`ontology`
============================

The heart and soul of your APIS application is the :term:`ontology`. It
describes :term:`entities<entity>` and :term:`relations<relation>`.

Given that APIS is based on `Django <https://www.djangoproject.com/>`_, the
file where we describe our entities and relations is the `models.py
<https://docs.djangoproject.com/en/4.2/topics/db/models/>`_ file of your APIS
project.

Entities
^^^^^^^^

Entities have to inherit from
:class:`apis_core.apis_entities.models.AbstractEntity`. Like with any other
Django model, you can define `model fields
<https://docs.djangoproject.com/en/4.2/ref/models/fields/>`_ describing the
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
migrations <https://docs.djangoproject.com/en/4.2/topics/migrations/>`_ your
models will show up in the APIS webinterface in ``Entities`` menu in the
top left corner.
For every :term:`entity` you defined there will be an overview page that
lists all instances for that :term:`entity`, as well as a form for creating,
updating, merging and deleting entities.

.. image:: img/ontology_entity_menu.png
   :alt: Image showing the APIS Entity menu with one item labelled Persons
