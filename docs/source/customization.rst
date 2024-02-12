Customization
=============

List views
----------

The list views consist of a `django-filters
<https://django-filter.readthedocs.io>`_ `filterset
<https://django-filter.readthedocs.io/en/stable/ref/filterset.html>`_ on the
left and a `django-tables <django-tables2.readthedocs.io/>`_ `table
<https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#table>`_
of results on the right side.

The default filterset used is
:class:`apis_core.generic.filtersets.GenericFilterSet`. You can override the
filterset for you models by defining a custom filterset class in
``you_app.filtersets``. The filterset has to be named ``<Modelname>FilterSet``,
so if you have a model ``Person`` in your app ``myproject``, the view looks for
the filterset ``myproject.filtersets.PersonFilterSet``. You can inherit from
:class:`apis_core.generic.filtersets.GenericFilterSet` and add your
customzations.

The default table used is :class:`apis_core.generic.tables.GenericTable`. You
can override the table for your models by defining a custom table class in
``your_app.tables``. The table class has to be named ``<Modelname>Table``, so
if you have a model ``Person`` in your app ``myproject``, the view looks for
the table class ``myproject.tables.PersonTable``. You can inherit from
:class:`apis_core.generic.tables.GenericTable` and add your customizations.
:class:`apis_core.generic.tables.GenericTable` also contains a handful of
useful `django table columns
<https://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#columns>`_
that you might want to use.

The base queryset that is used in the listview, which is then filtered using
the django-filters filter, is ``model.objects.all()`` - but you can override
the queryset by creating a custom queryset for your model in
``you_app.querysets``. The queryset function has to be named
``<Modelname>ListViewQueryset``, so if you have a model ``Person`` in your app
``myproject``, the view looks for the queryset
``myproject.querysets.PersonListViewQueryset``.

List view templates
^^^^^^^^^^^^^^^^^^^

The list view looks for templates using the ``_list.html`` suffix. It uses the
``generic/generic_list.html`` template as fallback, but you can use a custom
template using your model name, so if your model is ``myproject.Person`` then
you can use the ``myproject/person_list.html`` template to override the generic
template.

Create and Update views
-----------------------

The create and update view use the form
:class:`apis_core.generic.forms.GenericModelForm` by default. You can override
the form it uses by creating a custom form in ``you_app.forms``. The form class
has to be named ``<Modelname>Form``, so if you have a model ``Person`` in your
app ``myproject``, the view looks for the form class
``myproject.forms.PersonForm``.

Create and update view templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The create and update views looks for templates using the ``_form.html``
suffix. It uses the ``generic/generic_form.html`` template as fallback, but you
can use a custom template using your model name, so if your model is
``myproject.Person`` then you can use the ``myproject/person_form.html``
template to override the generic template.

Autocomplete views
------------------

The autocomplete views filter your model instances based on a query string
provided. By default, the autocomplete views use
:func:`apis_core.generic.helpers.generate_search_filter` to filter the model
queryset. You can override the queryset by creating a custom queryset for your
model in ``your_app.querysets``. The queryset function has to be named
``<Modelname>AutocompleteQueryset``, so if you have a model ``Person`` in your
app ``myproject``, the view looks for the queryset
``myproject.querysets.PersonAutocompleteQueryset``.

The results of the autocomplete view can be themed using templates. The
autocomplete view looks for templates using the ``autocomplete_result.html``
suffix, if no such template is found, the string representation of the result
is used. The autocomplete view uses the same template search function as for
other templates, so if you have a model ``myproject.Person`` then you can use
the ``myproject/person_autocomplete_result.html`` template.

The results of the autocomplete view can be extended with additional results
coming from another source (an external API or another queryset). The view
looks for this function in ``your_app.querysets`` and it has to be named
``<Modelname>ExternalAutocomplete``, so if you have a model ``Person`` in yoru
app ``myproject``, the view looks for the function in
``myproject.querysets.PersonExternalAutocomplete``.

Import view
-----------

The import view uses the form
:class:`apis_core.generic.forms.GenericImportForm` by default. You can override
the form it uses by creating a custom form in ``your_app.forms``. The form
class has to be named ``<ModelName>ImportForm``, so if you have a model
``Person`` in your app ``myproject``, the view looks for the form class
``myproject.forms.PersonImportForm``.

Import view template
^^^^^^^^^^^^^^^^^^^^

The import view looks for templates using the ``_import.html`` suffix. It uses
the ``generic/generic_import.html`` template as fallback, but you can use a
custom template using your model name, so if your model is ``myproject.Person``
then you can use the ``myproject/person_import.html`` template to override the
generic template.

Class, method and template lookup
---------------------------------

As mentioned above, APIS tries to find the correct class or method to override
the ones the ``generic`` one ships. This is done using
:func:`apis_core.generic.helpers.first_match_via_mro`. The method does not only
look for possible overrides using the name of the model itself, but also using
all the parent models following the full inheritance chain. So if all your models
inherit from ``MyAbstractModel``, you can for example create an override table
for all your models by creating a ``myproject.tables.MyAbstractModelTable``.
