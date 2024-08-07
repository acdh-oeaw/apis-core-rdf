Configuration
=============


``APIS_BASE_URL`` and :class:`apis_core.apis_entities.api_views.GetEntityGeneric`
---------------------------------------------------------------------------------

When you create an instance of an Entity a signal
:py:func:`apis_core.apis_entities.models.create_default_uri` is triggered that
tries to generate a canonical URI for the entity. The signal can be disabled by
setting the ``CREATE_DEFAULT_URI`` setting to ``False``.
If the signal runs, it creates the canoncical URI from two parts. The first part
comes from the ``APIS_BASE_URI`` setting. The second part comes from the reverse
route of ``GetEntityGenericRoot`` if that exists. If not, it uses the
the reverse route of ``apis_core:GetEntityGeneric``, which is defined in
:py:mod:`apis_core.urls` and defaults to ``/entity/{pk}``.

Django Settings
---------------

This section deals with the internal configuration of APIS. For instructions on how to set it up please refer
to :doc:`installation`.
All the settings described here are part of the Django settings and can be set in the ``settings.py`` file of your Django project.


REST_FRAMEWORK
^^^^^^^^^^^^^^

APIS uses the `Django Restframework <https://www.django-rest-framework.org/>`_ for API provisioning. Restframework specific settings like the default page size can be set here.

.. code-block:: python

    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
        "rest_framework.permissions.DjangoModelPermissions",
    )

Use the above default for allowing every user with permissions on a model to change all model instances.
Set ``"rest_framework.permissions.IsAuthenticated"`` if every logged in user should have all permissions.

.. code-block:: python

    REST_FRAMEWORK["PAGE_SIZE"] = 50

Sets the default page size the APIS RestAPI should deliver.


SPECTACULAR_SETTINGS
^^^^^^^^^^^^^^^^^^^^

We provide a custom schema generator for spectacular.
It is meant as a drop in replacement for the
``DEFAULT_GENERATOR_CLASS`` of drf-spectacular. You can use it like this:

.. code-block:: python

    SPECTACULAR_SETTINGS["DEFAULT_GENERATOR_CLASS"] = 'apis_core.generic.generators.CustomSchemaGenerator'


Background:

The first reason is, that we are using a custom converter
(:class:`apis_core.generic.urls.ContenttypeConverter`) to provide access to views
and api views of different contenttypes. The default endpoint generator of the
drf-spectacular does not know about this converter and therefore sees the
endpoints using this converter as *one* endpoint with one parameter called
``contenttype``. Thats not what we want, so we have to do our own enumeration -
we iterate through all contenttypes that inherit from ``GenericModel`` and
create schema endpoints for those programatically.

The second reason is, that the autoapi schema generator of DRF Spectacular
and our :class:`apis_core.generic.api_views.ModelViewSet` don't work well together.
Our ModelViewSet needs the dispatch method to set the model of the
``ModelViewSet``, but this method is not being called by the generator while
doing the inspection, which means the ``ModelViewSet`` does not know about the
model it should work with and can not provide the correct serializer and filter
classes. Therefore we create the callback for the endpoints by hand and set
the model from there.


APIS_BASE_URI
^^^^^^^^^^^^^

.. code-block:: python

    APIS_BASE_URI = "https://your-url-goes-here.com"

Sets the base URI your instance should use. This is important as APIS uses mainly URIs instead of IDs.
This setting is used to generate the canonical URI of an entity. It is included in the serializations 
of entities (eg the JSON returned by the API) and therefore should be set to the URL your production app
is running on.


APIS_NEXT_PREV
^^^^^^^^^^^^^^

.. code-block:: python
    
    APIS_NEXT_PREV = True


APIS_LIST_VIEWS_ALLOWED
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    APIS_LIST_VIEWS_ALLOWED = False


Sets whether list views are accessible for anonymous (not logged in) users.


APIS_DETAIL_VIEWS_ALLOWED
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    APIS_DETAIL_VIEWS_ALLOWED - False


Sets whether detail views are accessible for anonymous (note logged in) users.

APIS_VIEW_PASSES_TEST
^^^^^^^^^^^^^^^^^^^^^

Allows to define a function that receives the view as an argument - including
e.g. the `request` object - and can perform checks on any of the views
attributes. The function can, based on these checks, return a boolean which
decides if the request is successful or leads to a 403 permission denied.

APIS_LIST_VIEW_OBJECT_FILTER
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Allows to define a function that receives the view - including e.g. the
`request` object - and a queryset and can do custom filtering on that queryset.
This can be used to set the listviews to public using the
`APIS_LIST_VIEWS_ALLOWED` setting, but still only list specific entities.