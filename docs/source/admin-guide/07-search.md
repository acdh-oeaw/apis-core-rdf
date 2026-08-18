# Search

The [apis_core.search] module provides a way to create a search index over
different models. It uses a combination of simple search queries and PostgreSQLs
trigram search.

The functionality is based on the [`SearchEntry`][apis_core.search.models.SearchEntry]
model which stores a serialized version of the model instances data.

All models inheriting from [`GenericModel`][apis_core.generic.abc.GenericModel] are
being indexed automatically. If you want to exclude a model from being indexed, set the
`Config.index_for_search` attribute to `False`. If you want to include a model in the
index, set `Config.index_for_search` to `True`.

```
from django.db import models
from apis_core.generic.abc import GenericModel

class MyModel(GenericModel):
    class Config(GenericModel.Config):
        index_for_search = False
```


For every model instance an [`SearchEntry`][apis_core.search.models.SearchEntry] will be added
to the database, containing representations of the model instance optimized for
search. The [`SearchSerializer`][apis_core.search.serializers.SearchSerializer] class is used by
default to serialize the instance for search. It is based on
[django.core.serializers.json.Serializer] but for m2m fields it adds the values
instead of simply the keys.

To control which fields of the model should be serialized for search (and thus control
if the model instances come up in search results), you can set the `search_fields` parameter
n the `Config` subclass:

```
from django.db import models
from apis_core.generic.abc import GenericModel

class Person(GenericModel):
    forename = models.CharField()
    surname = models.CharField()
    long_description = models.TextField()

    class Config(GenericModel.Config):
        search_fields = {"forename", "surname"}
```

## m2m fields

As mentioned above, m2m fields are being serialized as the values of the model
they point to. If the instances of the ManyToManyField model change, the model
containing this pointer does not change automatically. You can define with
`m2m_fields` for which ManyToManyField the model should "follow" the updates.

```
from django.db import models
from apis_core.generic.abc import GenericModel

class Profession(GenericModel):
    name = models.CharField()

class Title(GenericModel):
    label = models.CharField()

@search.register(m2m_fields={"profession"})
class Person(GenericModel):
    forename = models.CharField()
    surname = models.CharField()
    profession = models.ManyToManyField(Profession)

    class Config(GenericModel.Config):
        search_follow_m2m = {"profession"}
```
In this case, when a profession is changed, the `SearchEntry`s of all `Person`s
that point to that profession are also updated.

## Management commant

There is an `initialize_search` management command that (re)creates the
SearchEntry instances for all registered models.
You can pass the `--content-types` argument to create the SearchEntry only
for a subset of models. You can pass the `--recreate` argument to recreate
existing search index entries.

## Weighting

The weighting logic annotates the search results with the result of the ranking
calculation. In the search result overview you can see a 🛈 symbol - hovering over
it shows the different numbers:

* First number: the greater value of: (title rank * 2, content rank)
* Second number: the title rank
* Third number: the content rank
* Fourth number: 10: title contains, 9: title contains case insensitive, 8:
  title slug contains, 7: title slug contains case insensitive, 6: content text
  contains, 5: content text contains case insensitive; 4: content text slug
  contains, 3: content text slug contains case insensitive
