# Search

The [apis_core.search] module provides a way to create a search index over
various models. It uses a combination of simple search queries and PostgreSQLs
trigram search.

To enable the module, add `apis_core.search` to the
[`INSTALLED_APPS`](https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-INSTALLED_APPS).
This will run the needed migrations to create the
[`SearchEntry`][apis_core.search.models.SearchEntry] and enable the
[TrigramExtension](https://docs.djangoproject.com/en/6.0/ref/contrib/postgres/operations/#trigramextension).

To register a model for the full text search, use the [apis_core.search.registry.search.register] decorator.

```
from django.db import models
from apis_core.search.registry import search

@search.register
class MyModel(models.Model): ...
```


For every model instance an [`SearchEntry`][apis_core.search.models.SearchEntry] will be added
to the database, containing representations of the model instance optimized for
search. The [`SearchSerializer`][apis_core.search.serializers.SearchSerializer] class is used by
default to serialize the instance for search. It is based on
[django.core.serializers.json.Serializer] but for m2m fields it adds the values
instead of simply the keys.

To control which fields of the model should be serialized for search (and thus control
if the model instances come up in search results), you can pass the `fields` parameter
to the [`@search.register`][apis_core.search.registry.search] decorator:

```
from django.db import models
from apis_core.search.registry import search

@search.register(fields={"forename", "surname"})
class Person(models.Model):
    forename = models.CharField()
    surname = models.CharField()
    long_description = models.TextField()
```

## m2m fields

As mentioned above, m2m fields are being serialized as the values of the model
they point to. If the instances of the ManyToManyField model change, the model
containing this pointer does not change automatically. You can define with
`m2m_fields` for which ManyToManyField the model should "follow" the updates.

```
from django.db import models
from apis_core.search.registry import search

class Profession(models.Model):
    name = models.CharField()

class Title(models.Model):
    label = models.CharField()

@search.register(m2m_fields={"profession"})
class Person(models.Model):
    forename = models.CharField()
    surname = models.CharField()
    profession = models.ManyToManyField(Profession)
```
In this case, when a profession is changed, the `SearchEntry`s of all `Person`s
that point to that profession are also updated.

## Management commant

There is an `initialize_search` management command that (re)creates the
SearchEntry instances for all registered models.
You can pass the `--content-types` argument to (re)create the SearchEntry only
for a subset of models.
