Importing data from external resources
======================================

APIS provides the structure for easily importing data from external resources.
One main component for this are `Importer` classes. They always belong to a
Django Model, reside in the same app as the Djang model in the `importers`
module and are named after the Django Model. So if you have an app called
`myapp` with a `models.py`

.. code-block:: python

   class Person(models.Model):
        name = models.CharField(max_length=255)

then the respective importer should reside in `myapp.importers` and has to be
called `PersonImporter`.

An importer takes two arguments to instantiate: an `uri` and a `model`. The
importers task is then to create a model instance from this URI, usually by
fetching data from the URI, parsing it and extracting the needed fields.
The instance should then be returned by the `create_instance` method of the
importer. There is :py:class:`apis_core.generic.importers.GenericImporter`
which you can inherit from.

To use this logic in forms, there is
:py:class:`apis_core.generic.forms.fields.ModelImportChoiceField` which is
based on `django.forms.ModelChoiceField`. It checks if the passed value starts
with `http` and if so, it uses the importer that fits the model and uses it to
create the model instance.
