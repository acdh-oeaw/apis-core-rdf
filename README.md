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

APIS contains the ["Material Symbols" font](https://fonts.google.com/icons)(commit ace1af0), which
is licensed under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).
The Swagger Logo in `core/static/img` comes from [wikimedia
commons](https://commons.wikimedia.org/wiki/File:Swagger-logo.png) and is
licensed under the [Creative Commons Attribution-Share Alike 4.0 International
license](https://creativecommons.org/licenses/by-sa/4.0/deed.en)
The Git Logo in `core/static/img` comes from [the git scm website](https://git-scm.com/downloads/logos)
ans is licensed under the [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/).


Installation
------------
<!-- Installation -->
Create a project using your favorite package manager:

```shell
poetry new foobar-repository
```

In your project folder, add apis as a dependency (replace `RELEASE_VERSION`
with the version you want to install):

```shell
poetry add git+https://github.com/acdh-oeaw/apis-core-rdf#RELEASE_VERSION
```

Now remove the generated `__init__.py` (because `django-admin` wants to be the
one that creates that) and setup your Django project
```shell
rm -f foobar_repository/__init__.py
poetry run django-admin startproject foobar_repository .
```

Now start using your Django project
```shell
poetry run ./manage.py runserver
```

To use the APIS framework in your application, you will need to add the following dependencies to
[`INSTALLED_APPS`](https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps):

```python
INSTALLED_APPS = [
    # our main app, containing the ontology (in the `models.py`)
    # and our customizations
    "sample_project",
    # `apis_override_select2js` is a workaround for APIS'
    # handling of autocomplete forms. It should be listed
    # at the beginning of the list, to make sure the
    # files shipped with it are served in precedence.
    "apis_override_select2js",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ui stuff used by APIS
    "crispy_forms",
    "crispy_bootstrap4",
    "django_filters",
    "django_tables2",
    "dal",
    "dal_select2",
    # REST API
    "rest_framework",
    # swagger ui generation
    "drf_spectacular",
    # The APIS apps
    "apis_core.core",
    "apis_core.generic",
    "apis_core.apis_metainfo",
    "apis_core.apis_relations",
    "apis_core.apis_entities",
    # apis_vocabularies is deprecated, but there are
    # still migrations depending on it - it will be dropped
    # at some point
    "apis_core.apis_vocabularies",
    # APIS collections provide a collection model similar to
    # SKOS collections and allow tagging of content
    "apis_core.collections",
    # APIS history modules tracks changes of instances over
    # time and lets you revert changes
    "apis_core.history",
]
```

Finally, add the APIS urls to your applications [URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)

```python
urlpatterns = [
    path("", include("apis_core.urls", namespace="apis")),
    # https://docs.djangoproject.com/en/stable/topics/auth/default/#module-django.contrib.auth.views
    path("accounts/", include("django.contrib.auth.urls")),
    # https://docs.djangoproject.com/en/stable/ref/contrib/admin/#hooking-adminsite-to-urlconf
    path("admin/", admin.site.urls),
]
```

Now you should be ready to roll. Start [creating your ontology](https://acdh-oeaw.github.io/apis-core-rdf/ontology.html).
