Settings
========

This section deals with the internal configuration of the APIS tool. For instructions on how to set it up please refer
to :doc:`installation`.


REST_FRAMEWORK
--------------

APIS uses the `Django Restframework`_ for API provisioning. Restframework specific settings like the default page size can be set here.

.. code-block:: python

    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
        "rest_framework.permissions.DjangoObjectPermissions",
    )

Use the above default to allow setting permissions on object level. Meaning that every user gets his permissions depending on his/her user group and the collections this group has permissions for.
Set ``"rest_framework.permissions.DjangoModelPermissions"`` for allowing every user with permissions on a model to change all model instances.
Set ``"rest_framework.permissions.IsAuthenticated"`` if every logged in user should have all permissions.

.. code-block:: python

    REST_FRAMEWORK["PAGE_SIZE"] = 50

Sets the default page size the APIS RestAPI should deliver.


APIS_BASE_URI
-------------

.. code-block:: python

    APIS_BASE_URI = "https://your-url-goes-here.com"

Sets the base URI your instance should use. This is important as APIS uses mainly URIs instead of IDs. These URIs are also used for the serialization.


APIS_NEXT_PREV
--------------

.. code-block:: python
    
    APIS_NEXT_PREV = True


APIS_API_ID_WRITABLE
---------------------

.. code-block:: python

    APIS_API_ID_WRITABLE = False


Boolean setting for defining if the `id` field of an entity is writable via the
API. Defaults to false. You can set it to `True` if you want to import entities
from another instance and want to keep the `id`.


APIS_LIST_VIEWS_ALLOWED
-----------------------

.. code-block:: python

    APIS_LIST_VIEWS_ALLOWED = False


Sets whether list views are accessible for anonymous (not logged in) users.


APIS_DETAIL_VIEWS_ALLOWED
-------------------------

.. code-block:: python
    
    APIS_DETAIL_VIEWS_ALLOWED - False


Sets whether detail views are accessible for anonymous (note logged in) users.

APIS_VIEW_PASSES_TEST
---------------------

Allows to define a function that receives the view as an argument - including
e.g. the `request` object - and can perform checks on any of the views
attributes. The function can, based on these checks, return a boolean which
decides if the request is successful or leads to a 403 permission denied.

APIS_LIST_VIEW_OBJECT_FILTER
----------------------------

Allows to define a function that receives the view - including e.g. the
`request` object - and a queryset and can do custom filtering on that queryset.
This can be used to set the listviews to public using the
`APIS_LIST_VIEWS_ALLOWED` setting, but still only list specific entities.
