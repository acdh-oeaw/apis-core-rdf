---
title: Additional Features
---

APIS is designed to be extensible and customizable. This section
describes some additional features that are shipped with APIS and how to
use them.

# History plugin

The [apis_core.history][] module provides
versioning for APIS. It is based on the
[django-simple-history](https://django-simple-history.readthedocs.io/en/latest/)
package.

## Track changes by users

To record the user who made a change, the
`django-simple-history` module used by APIS provides a
middleware that sets the `history_user` attribute of the
request object to the current user. It then saves this information to
the `history_user` attribute of the historical record. To
activate the middleware, add
`simple_history.middleware.HistoryRequestMiddleware` to your
`MIDDLEWARE` setting:

``` python
MIDDLEWARE = [
    ...
    'simple_history.middleware.HistoryRequestMiddleware',
    ...
]
```

## VersionMixin

The [apis_core.history.models.VersionMixin][] class is a mixin that can be added to any model to enable
versioning. It adds a `history` property to the model that
returns a `HistoricalRecords` instance. Additionally, it
allows to override the date of the revision by setting the
`_history_date` property of the model instance. To activate
versioning for a model, simply inherit from `VersionMixin`:

``` python
from django.db import models
from apis_core.apis_history.models import VersionMixin

class MyModel(VersionMixin, models.Model):
    pass
```

## API endpoint

The [apis_core.history.api_views.GenericHistoryLog][] class is a viewset that provides a REST API endpoint for
the version history of a model. It can be used to retrieve the version
history of a model instance. The viewset can be accessed under
`/apis/api/entity_combined/<contenttype:contenttype>/<int:pk>/`.
It takes two mandatory URL parameters: `pk` and
`contenttype`. The `pk` parameter is the primary
key of the model instance and the `contenttype` parameter is
the name of the model class. The viewset returns a list of historical
revisions of the model instance. It is also included in the
`apis_core` API schema. The swagger documentation can be
accessed under
`/apis/swagger/schema/swagger-ui/#/apis/apis_api_history_entity_edit_log_list`.

## Management commands

The APIS history plugin, based on `django-simple-history`,
provides several management commands to help curate history objects.
Here are some of the most useful commands:

# 1. Populate history tables

``` bash
python manage.py populate_history --auto
```

This command populates history tables with the current state of the
models. It's particularly useful when you've added
`VersionMixin` to an existing model. The
`--auto` flag applies the command to all tracked models, or
you can specify a list of models instead.

# 2. Clean duplicate history entries

``` bash
python manage.py clean_duplicate_history --auto
```

This command removes duplicate history entries.
`django-simple-history` creates a history object every time
`save()` is called on an object, regardless of whether any
changes were made. This command deletes history objects that are
identical to the previous entry.

# 3. Remove old history entries

``` bash
python manage.py clean_old_history --days 60 --auto
```

This command deletes history entries older than the specified number of
days (60 in this example).

For more information on these and other management commands, refer to
the [django-simple-history
documentation](https://django-simple-history.readthedocs.io/en/latest/utils.html).

# Collections plugin

APIS includes models to make working with collections easier. These
can be used to build vocabularies or a tagging solution or even a
workflow solution. To use it, you have to add
`apis_core.collections` to your
`INSTALLED_APPS`.

The `collections` module consists of the two models
[apis_core.collections.models.SkosCollection][] and
[apis_core.collections.models.SkosCollectionContentObject][].
The former is the class for the collection
vocabularies, whereas the latter lets you connect specific collections
with any content instance, using generic relations.

You can create your collections in the `admin` interface or
using the `generic` app.

If you want to use collections to provide choices for a form, you can
either use a [django.models.ForeignKey][] or use a
[django.models.CharField][] and you
customize the model form to use the collection as choices for this
field. Both approaches have pros and cons.

There are a couple of templatetags that make working with collection
easier. They all reside in the
[apis_core.collections.templatetags.apis_collections][] templatetag library. If you use them, you have to include
[apis_core.collections.urls][] into your
urls.py, for example like this:

``` python
urlpatterns = [
    ...
    path("apis/collections/", include("apis_core.collections.urls")),
    ...
]
```

The templatetags are:

-   [apis_core.collections.templatetags.apis_collections.collection_toggle][]
-   [apis_core.collections.templatetags.apis_collections.collection_toggle_by_id][]

This templatetag takes the instance of an object and a collection (or,
in the case of `_by_id`, the id of a collection) and lets
the user create and remove the connection between this instance and the
collection.

-   [apis_core.collections.templatetags.apis_collections.collection_session_toggle_by_id][]

This templatetag provides a checkbox that enables a collection as
"session collection" - this means that if enabled, all new versions of
instances will be added to this collection. This is implemented in
[apis_core.collections.signals.add_to_session_collection][].
To use this feature, [apis_core.history][] has to be enabled
and [crum.CurrentRequestUserMiddleware][] has to be added to `MIDDLEWARE`
