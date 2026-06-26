---
title: Overview
---

ANERO is a framework for providing a web platform for collecting data and for
maintaining that data in a structured form. ANERO is based on the
[Django](https://www.djangoproject.com/) web framework, which is written in the
[Python](https://www.python.org) programming language. ANERO is therefore also
written in Python.

For every project that uses ANERO, there is a separate *instance* that uses its
own database. That means a project has its own space for its own data. But it
is also possible to import data from other projects or from external sources.

<div class="highlight-block" markdown="1">
At the ACDH every ANERO instance has its own *repository*. The repository is
the place where the code of the instance is stored. Currently all ACDH ANERO
repositories reside at the public code hosting platform
[GitHub](https://github.com). All the repositories are **public**.
</div>

# ANERO Building Blocks

ANERO is built of different modules that provide various functionality. Those
modules all have various settings to adapt them to different use cases. Every
module has links to its data in the menu bar at the top of the ANERO interface.

The main module of ANERO is the `generic` module, that provides the basic
interfaces for *creating*, *reading*, *updating*, *merging*, *enriching*,
*duplicating*, and *deleting* data. It does that by providing web forms where
data can be entered. Then there is a tabular listing of the data that already
exists. Every entry in this list has a button for viewing the details, for
updating the entry, for deleting the entry and for duplicating (or copying) the
entry. It is also possible to import data from other web sources, for example
from [wikidata](https://www.wikidata.org/) or
[geonames](https://www.geonames.org/).

The page that shows the tabular listing also provides a filter. This is useful
if there is a lot of data. Those types of filters that are available are
automatically generated for the type of data that is listed, but they can be
adapted (more on that later).

All data that is managed in ANERO uses the `generic` module.

Another module of ANERO is then `entities` module. Entities have additional
features:

* They have a separate menu item in the top bar
* Every entity gets a URI as a static identifier

The next module is the `relations` module. Similar to entities, relations have
a separate entry in the main menu. Relations define how data entries in ANERO
relate to one another. Relations point to a subject and an object and link
those two together.

Then there is the `collections` module. Collections allow grouping data
together. A synonym for collections would be *tags*.

At last there are helper modules: the `search` module and the `documentation`
module. The `search` module allows doing a wider search. The mentioned filter
in the tabular listing of the `generic` module only allows filtering data of
one specific type. The `search` module provides a search index to search over
different kinds of data. The `documentation` provides an overview of the data
that can be entered. It provides a graphic representation of the *data model*.

# The Data Model

The first step before you can start using ANERO, is to define a [data
model](https://en.wikipedia.org/wiki/Data_model) that represents the data that
you want to enter and maintain in ANERO. No worries, that data model is not set
in stone and can change over time and it usually does. The data model is a
first structured view on the data you are working with.

<div class="highlight-block" markdown="1">
At the ACDH you are usually in a team with a technician. The technician well
help you defining your data model and will also write the code for the
data model and update it if necessary.
</div>

Usual types of data that are managed in ANERO instances are for example
**persons** and **places**. But its also possible to manage animals or
celestial objects. For every type of data, attributes of that datatype can be
defined.

A person for example has a *forename* and a *surname* and a *date of birth*. A
place has a *label* and *coordinates*.

In ANERO, both `person` and `place` are usually defined as entities. A person
can also have a profession. The profession can be modelled in different ways-
every profession could be a collection for example. But given that there might
be a lot of different professions, usually a separate profession type is
created, but it is not an entity itself. The person then gets an attribute
*profession* that can be one of the profession types.

To store relationships between persons and places in ANERO, relations can be
defined, for example *born in* or *lived in*. These relations can themselves
have attributes: a person lives in a place for a period of time, so the *lives
in* relations gets a *start date* and an *end date*.
