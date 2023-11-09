APIS
====

![Django Tests](https://github.com/acdh-oeaw/apis-core-rdf/actions/workflows/django-tests.yml/badge.svg)
![GitHub release (with filter)](https://img.shields.io/github/v/release/acdh-oeaw/apis-core-rdf)

The *Austrian Prosophographic Information System* is a
[Django](https://www.djangoproject.com/) based prosopography framework. It
allows to create web applications to manage both entities and relations between
entities. It provides API access to the data in various formats and creates
swagger defintions. A swagger-ui allows for comfortable access to the data.

Data can also be imported from remote resources described in
[RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework).

In addition to this configurable import of data via RDF, there is also an
configurable serialization of data. The generic RestAPI of APIS provides data
either in the internal JSON format, TEI or RDF (serialized with *CIDOC CRM*). 

APIS comes with a built in system of autocompletes that allows researchers to
import meta-data of entities with just a single click. Out of the box APIS
supports Stanbol as a backend for the autocompletes, but the system is rather
easy to adapt to any Restfull API. APIS also supports the parsing of RDFs
describing entities into an entity. The parsing is configured in a settings
file.

*Entities*

*Relations*

Licensing
---------

All code unless otherwise noted is licensed under the terms of the MIT License
(MIT). Please refer to the file LICENSE.txt in the root directory of this
repository.

All documentation and images unless otherwise noted are licensed under the
terms of Creative Commons Attribution-ShareAlike 4.0 International License. To
view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/


Installation
------------

Create a project using your favourite package manager:

```shell
poetry new foobar-repository --name apis_ontology
```

Currently (as of 2023-10) the name of the apis application **has** to be
`apis_ontology` - this is considered a bug and is tracked in [this bug
report](https://github.com/acdh-oeaw/apis-core-rdf/issues/100).

In your project folder, add apis as a dependency:

```shell
poetry add git+https://github.com/acdh-oeaw/apis-core-rdf#v0.6.1
```

Setup your Django project
```shell
poetry run django-admin startproject foobar_django_project .
```

Now start using your Django project
```shell
poetry run ./manage.py runserver
```

To use the APIS framework in your application, you will need to add the following dependencies to
[`INSTALLED_APPS`](https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps):

```python
# `apis_override_select2js` is a workaround for APIS' handling of autocomplete
# forms. It should be listed at the beginning of the list, to make sure the
# files shipped with it are served in precedence.
"apis_override_select2js",

# ui stuff used by APIS
"crispy_forms",
"django_filters",
"django_tables2",
"dal",
"dal_select2",

# api
"rest_framework",
"rest_framework.authtoken",

# for swagger ui generation
"drf_spectacular",

# Your ontology
"apis_ontology",

# The APIS apps
"apis_core.core",
"apis_core.apis_entities",
"apis_core.apis_metainfo",
"apis_core.apis_relations",
"apis_core.apis_vocabularies",
"apis_core.apis_labels",

```

Also, add the following two [context processors](https://docs.djangoproject.com/en/4.2/ref/templates/api/#django.template.RequestContext):
```
# we need this for listing entities in the base template
"apis_core.context_processors.custom_context_processors.list_entities",
# we need this for accessing `basetemplate`
"apis_core.context_processors.custom_context_processors.list_apis_settings",
```

Finally, add the APIS urls to your applications [URL Dispatcher](https://docs.djangoproject.com/en/4.2/topics/http/urls/):
```python
from django.urls import include
from apis_core.apis_entities.api_views import GetEntityGeneric
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # APIS refers to the `login` and `logout` urls in its `base.html` template
    # you can define your own or use the ones shipped with Django
    path("accounts/", include("django.contrib.auth.urls")),
    # The APIS views
    path("apis/", include("apis_core.urls", namespace="apis")),
    # It is common for APIS projects to have a shortcut for accessing entities
    path(
        "entity/<int:pk>/", GetEntityGeneric.as_view(), name="GetEntityGenericRoot"
    ),
]

urlpatterns += staticfiles_urlpatterns()
```

Now you should be ready to roll. Start creating your entities in you `apis_ontology/models.py`.
