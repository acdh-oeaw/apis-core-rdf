Extending autocomplete results
==============================

The autocomplete endpoint :py:class:`apis_core.generic.views.Autocomplete` can
be extended to provide additional autocomplete results, that are not
based on the default Django querysets. The autocomplete view always refers to a
Django model. To extend the results for a specific model, you have to create an
`ExternalAutocomplete` class, that is named after the model and resides in the
`querysets` module in the same app. So if you have an app called `myapp` with a
`models.py`

.. code-block:: python

   class Person(models.Model):
        name = models.CharField(max_length=255)

then the respective autocomplete class should reside in `myapp.querysets` and
has to be called `PersonExternalAutocomplete`.

.. code-block:: python

    class PersonExternalAutocomplete:
        def extract_results(data):
            ... do something with the data
            return data

        def get_results(self, q):
            with urllib.request.urlopen(f"https://some.uri.tld/search?q={q}") as f:
                data = extract_results(json.loads(f.read()))
                return results
            return {}

The class has to have a `get_results` method that receives a query as the first
parameter and returns a result in the format, the `django-autocomplete-light`
module uses- this is a dict with the keys "id", "text" and "selected_text".
