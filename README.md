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
is licenced under the [Apache Licence Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).


Installation
------------

Create a project using your favourite package manager:

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
[`INSTALLED_APPS`](https://docs.djangoproject.com/en/4.2/ref/settings/#installed-apps):

https://github.com/acdh-oeaw/apis-core-rdf/blob/9135728495be144d228adbdc77a392d75a617bdb/sample_project/settings.py#L17-L59

Finally, add the APIS urls to your applications [URL Dispatcher](https://docs.djangoproject.com/en/4.2/topics/http/urls/)

https://github.com/acdh-oeaw/apis-core-rdf/blob/9135728495be144d228adbdc77a392d75a617bdb/sample_project/urls.py#L4-L10

Now you should be ready to roll. Start creating your entities in you `apis_ontology/models.py`.
