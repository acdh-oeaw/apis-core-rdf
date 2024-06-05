History plugin
==============

The :py:mod:`apis_core.history` module provides versioning 
to the APIS framework. It is based on the `django-simple-history`_
package.

VersionMixin
------------

The :class:`apis_core.history.models.VersionMixin` class is a mixin
that can be added to any model to enable versioning. It adds a `history`
property to the model that returns a `HistoricalRecords` instance. Additionally
it allows to override the date of the revision by setting the `_history_date`
property of the model instance.
To activate versioning for a model, simply inherit from `VersionMixin`:

.. code-block:: python

    from django.db import models
    from apis_core.apis_history.models import VersionMixin

    class MyModel(VersionMixin, models.Model):
        pass



API endpoint
------------

The :class:`apis_core.history.api_views.GenericHistoryLog` class is a viewset
that provides a REST API endpoint for the version history of a model. It can be
used to retrieve the version history of a model instance.
The viewset can be accessed under `/apis/api/history/entity/edit_log/`. It takes
two mandatory query parameters: `id` and `entity_type`. The `id` parameter is the
primary key of the model instance and the `entity_type` parameter is the name of
the model class. The viewset returns a list of historical revisions of the model
instance. It is also included in the `apis_core` API schema. The swagger documentation
can be accessed under `/apis/swagger/schema/swagger-ui/#/apis/apis_api_history_entity_edit_log_list`.


.. _django-simple-history: https://django-simple-history.readthedocs.io/en/latest/
