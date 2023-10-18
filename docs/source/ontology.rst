Set up your ontology
====================

APIS provides two main types: entities and relations. Entities are things, whereas relations are the connections between things.
To define your own entities and relations, we use `Django models <https://docs.djangoproject.com/en/4.2/topics/db/models/>`_.

Entities
--------

To create entities, define them in your application and let them inherit from :class:`apis_core.apis_entities.models.AbstractEntity`
Like with any other Django model, you can define fields describing the attributes of this entity:

.. code-block:: python

   from apis_core.apis_entities.models import AbstractEntity

   class Person(AbstractEntity):
       name = models.CharField(max_length=255, help_text="The persons´s name", blank=True, null=True)


   class Place(AbstractEntity):
       lat = models.FloatField(blank=True, null=True, verbose_name="latitude")
       lng = models.FloatField(blank=True, null=True, verbose_name="longitude")

For every entity you define, there will be a menu entry in the main APIS menu, pointing to a list of instances of this entity. In
this list it is possible to filter entities based on their defined attributes.
