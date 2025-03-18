Configuration
=============


``APIS_BASE_URI`` and :class:`apis_core.apis_entities.api_views.GetEntityGeneric`
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
If the value of ``APIS_BASE_URI`` changes and urls containing the former ``APIS_BASE_URI`` remain in the database, then the old ``APIS_BASE_URI`` value must added to the setting ``APIS_FORMER_BASE_URIS``.
``APIS_FORMER_BASE_URIS`` is a list that contains base urls that were once used.

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


APIS_ANON_VIEWS_ALLOWED
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    APIS_ANON_VIEWS_ALLOWED = False

Sets whether list and detail views are accessible for anonymous (not logged in) users.
If only a subset of the data should be exposed to the anonymous user, use `custom managers <https://docs.djangoproject.com/en/stable/topics/db/managers/#custom-managers>`_.


Maintenance Middleware
^^^^^^^^^^^^^^^^^^^^^^

APIS ships a maintenance middlware that you can use and activate to enable a maintenance mode in your project.
Maintenance mode means that only superuser accounts can access the webinterfaces, all other requests are being
answered with a simple maintenance mode page (the ``maintenance.html`` template).
To use the middleware, add

.. code-block:: python

   "apis_core.core.middleware.MaintenanceMiddleware"

to your ``settings.MIDDLEWARE`` list. To activate the maintenance mode once the middlware is enabled, simply
create a file ``apis_maintenance`` in the directory the main Django process runs in.
The path of the maintenance file can be changed in the settings: ``APIS_MAINTENANCE_FILE = "path of the file"``
