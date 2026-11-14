# Overview

{{ project_name }} is a Django based data management system, that is primarily
developed to allow data collection for prosopographic research. It is a
framework that allows to create web applications to manage both entities and
relations between entities.
{{ project_name }} provides API access to the data in various formats and
creates swagger defintions. A swagger-ui allows for comfortable access to the
data.

Data can also be imported from remote resources described in RDF.

In addition to this configurable import of data via RDF, there is also an
configurable serialization of data. The generic RestAPI of {{ project_name }}
provides data either in the internal JSON format, TEI or RDF (serialized with
CIDOC CRM).

{{ project_name }} comes with a built in system of autocompletes that allows
researchers to import meta-data of entities with just a single click. Out of
the box {{ project_name }} supports Stanbol as a backend for the autocompletes,
but the system is rather easy to adapt to any Restfull API. {{ project_name }}
also supports the parsing of RDFs describing entities into an entity. The
parsing is configured in a settings file.


```{toctree}
:hidden:
:caption: 🛠️ Administration

admin/installation.md
admin/ontology.md
admin/configuration.md
admin/customization.md
admin/features.md
admin/search.md
```

```{toctree}
:hidden:
:caption: 👩🏻‍💻 User-Guide

user/overview.md
user/glossary.md
```

```{toctree}
:hidden:
:caption: 🏗️ Development

develop/_changelog.md
develop/index.md
../apidocs/index.rst
```
