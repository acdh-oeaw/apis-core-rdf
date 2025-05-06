---
title: Customization
---

APIS is designed to be easily customizable. This section describes how
you can customize the views and the templates of the views that are
shipped with APIS by injecting classes and methods that are then
automatically used by the generic views. The core of the logic described
here is based on [apis_core.generic][].
It provides generic CRUD views and API views for all models that are
configured to use it. To make a model use the generic functionality, it
has to inherit from
[apis_core.generic.abc.GenericModel][]. In
standard APIS those models are:

-   [apis_core.apis_metainfo.models.RootObject][]
-   [apis_core.apis_metainfo.models.Uri][]
-   [apis_core.relations.models.Relation][]
-   [apis_core.collections.models.SkosCollection][]
-   [apis_core.collections.models.SkosCollectionContentObject][]

The [apis_core.history][] module also
uses the generic views for its models. This means that you can use the
generic views for the historical models of your own ontology. E.g. if
you have a model `Person` in your `your_app.models` module, you can use
the generic views for it. `/apis/your_app.historicalperson/` will be the
URL for the list view of the historical model.
`/apis/api/your_app.historicalperson/` for the API view.

If you want to use the generic app for your own model, simply make your
model inherit from
[apis_core.generic.abc.GenericModel][].

# List views

The list views consist of a
[django-filters](https://django-filter.readthedocs.io)
[filterset](https://django-filter.readthedocs.io/en/stable/ref/filterset.html)
on the left and a [django-tables](https://django-tables2.readthedocs.io/)
[table](https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#table)
of results on the right side.

The default filterset used is
[apis_core.generic.filtersets.GenericFilterSet][]. You can override the filterset for you models by defining
a custom filterset class in `your_app.filtersets`. The filterset has to
be named `<Modelname>FilterSet`, so if you have a model `Person` in your
app `myproject`, the view looks for the filterset
`myproject.filtersets.PersonFilterSet`. You can inherit from
[apis_core.generic.filtersets.GenericFilterSet][] and add your customizations.

The default table used is
[apis_core.generic.tables.GenericTable][].
You can override the table for your models by defining a custom table
class in `your_app.tables`. The table class has to be named
`<Modelname>Table`, so if you have a model `Person` in your app
`myproject`, the view looks for the table class
`myproject.tables.PersonTable`. You can inherit from
[apis_core.generic.tables.GenericTable][] and add your customizations.
[apis_core.generic.tables.GenericTable][] also contains a handful of useful [django table
columns](https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#columns)
that you might want to use.

Your table can also contain a `paginate_by` attribute, which is then
used by the list view to determine the number of items per page. When
this is not set, the page size defaults to `25`. To disable pagination
altogether, use `table_pagination = False`.

The base queryset that is used in the list view, which is then filtered
using the django-filters filter, is `model.objects.all()` - but you can
override the queryset by creating a custom queryset for your model in
`your_app.querysets`. The queryset function has to be named
`<Modelname>ListViewQueryset`, so if you have a model `Person` in your
app `myproject`, the view looks for the queryset
`myproject.querysets.PersonListViewQueryset`.

## List view templates

The list view looks for templates using the `_list.html` suffix. It uses
the `generic/generic_list.html` template as fallback, but you can use a
custom template using your model name, so if your model is
`myproject.Person` then you can use the `myproject/person_list.html`
template to override the generic template.

# Create and update views

The create and update views use the form
[apis_core.generic.forms.GenericModelForm][] by default. You can override the form they use by creating
a custom form in `your_app.forms`. The form class has to be named
`<Modelname>Form`, so if you have a model `Person` in your app
`myproject`, the view looks for the form class
`myproject.forms.PersonForm`.

## Create and update view templates

The create and update views look for templates using the `_form.html`
suffix. They use the `generic/generic_form.html` template as fallback,
but you can use a custom template using your model name, so if your
model is `myproject.Person`, you can use the
`myproject/person_form.html` template to override the generic template.

# Autocomplete views

The autocomplete views filter your model instances based on a query
string provided. By default, the autocomplete views use
[apis_core.generic.helpers.generate_search_filter][] to filter the model queryset. You can override the queryset
by creating a custom queryset for your model in `your_app.querysets`.
The queryset function has to be named `<Modelname>AutocompleteQueryset`,
so if you have a model `Person` in your app `myproject`, the view looks
for the queryset `myproject.querysets.PersonAutocompleteQueryset`.

The results of the autocomplete view can be themed using templates. The
autocomplete view looks for templates using the
`autocomplete_result.html` suffix; if no such template is found, the
string representation of the result is used. The autocomplete view uses
the same template search function as for other templates, so if you have
a model `myproject.Person` then you can use the
`myproject/person_autocomplete_result.html` template.

The results of the autocomplete view can be extended with additional
results coming from another source (an external API or another
queryset). The view looks for this function in `your_app.querysets` and
has to be named `<Modelname>ExternalAutocomplete`, so if you have a
model `Person` in your app `myproject`, the view looks for the function
in `myproject.querysets.PersonExternalAutocomplete`.

Let's say you have an app called `myapp` with the following `models.py`:

``` python
class Person(models.Model):
     name = models.CharField(max_length=255)
```

then the respective autocomplete class should reside in
`myapp.querysets` and has to be called `PersonExternalAutocomplete`.

``` python
class PersonExternalAutocomplete:
    def extract_results(data):
        ... do something with the data
        return data

    def get_results(self, q):
        with urllib.request.urlopen(f"https://some.uri.tld/search?q={q}") as f:
            data = extract_results(json.loads(f.read()))
            return results
        return {}
```

The class has to have a `get_results` method that receives a query as
the first parameter and returns a result in the format the
[django-autocomplete-light](https://django-autocomplete-light.readthedocs.io/)
module uses - a dict with the keys `id`, `text` and `selected_text`.

# Import view

The import view uses the form
[apis_core.generic.forms.GenericImportForm][] by default. You can override the form it uses by creating
a custom form in `your_app.forms`. The form class has to be named
`<ModelName>ImportForm`, so if you have a model `Person` in your app
`myproject`, the view looks for the form class
`myproject.forms.PersonImportForm`.

## Import view template

The import view looks for templates using the `_import.html` suffix. It
uses the `generic/generic_import.html` template as fallback, but you can
use a custom template using your model name, so if your model is
`myproject.Person`, you can use the `myproject/person_import.html`
template to override the generic template.

# Class, method and template lookup

As mentioned above, APIS tries to find the correct class or method to
override the ones `generic` ships. This is done using
[apis_core.generic.helpers.first_match_via_mro][]. The method does not only look for possible overrides using
the name of the model itself, but also using all the parent models
following the full inheritance chain. So if all your models inherit from
`MyAbstractModel`, you can for example create an override table for all
your models by creating a `myproject.tables.MyAbstractModelTable`.

# Importing data from external resources

APIS provides the structure for easily importing data from external
resources. One main component for this are `Importer` classes. They
always belong to a Django model, reside in the same app as the Django
model in the `importers` module and are named after the Django model. So
if you have an app called `myapp` with the following `models.py`:

``` python
class Person(models.Model):
     name = models.CharField(max_length=255)
```

then the respective importer should reside in `myapp.importers` and has
to be called `PersonImporter`.

An importer takes two arguments to instantiate: an `uri` and a `model`.
The importers task is then to create a model instance from this URI,
usually by fetching data from the URI, parsing it and extracting the
needed fields. The instance should then be returned by the
`create_instance` method of the importer. There is
[apis_core.generic.importers.GenericModelImporter][] which you can inherit from. It is used by default if no
other importer is defined for the model and tries to do the right
thing out of the box: it first looks if there is an RDF configuration
for the URI and if that fails tries to parse the URI response as JSON.

To use this logic in forms, there is
[apis_core.generic.forms.fields.ModelImportChoiceField][] which is based on
[django.forms.ModelChoiceField](https://docs.djangoproject.com/en/stable/ref/forms/fields/#modelchoicefield).
It checks if the passed value starts with `http` and if so, it uses the
importer that fits the model and uses it to create the model instance.

# Using the GenericModelImporter to import RDF

The [apis_core.generic.importers.GenericModelImporter][]
tries to parse the passed URI using the
[apis_core.utils.rdf][] module. This
module looks at all the existing models and uses the models
`rdf_configs` class methods to get a list of potential
RDF-Import config files. Those RDF-Import config files are
[TOML](https://toml.io/) configuration files. They have three main
attributes, which are `filters`, `attributes` and `relations`.

The `filters` attributes are key-value pairs that define filters that
have to match on the input data. Multiple `filters` entries can be
defined; only one of them has to match. Every `filters` entry can
contain multiple key-value pairs, which ALL have to match:

``` toml
[[filters]]
"rdf:type" = "gndo:DifferentiatedPerson"
```

The `attributes` config option lists key-value pairs which map keys
(usually model attributes) to a single SPARQL query or a list of SPARQL
queries. Instead of SPARQL it is also possible to simply write a compact
URI which is then looked up in the graph that results from the data
input:

``` toml
[attributes]
forename = ["gndo:forename", "gndo:preferredNameEntityForThePerson/gndo:forename"]
```

The `relations` config option lists mappings from a natural key of a
relation model to a dict containing a `curie` key with a compact URI or
a list of compact URIs and an `obj` or `subj` key defining the relations
other type (which will be used to import the data from the URI).

``` toml
[relations]
"apis_ontology.starbin" = { curies = "gndo:placeOfDeath", obj = "apis_ontology.place" }
```
