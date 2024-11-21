Development
===========

Dependencies
------------

* Django
* djangorestframework
* django-filter
* django-autocomplete-light
* django-crum
* django-crispy-forms
* django-tables2
* rdflib
* drf-spectacular
* requests
* django-model-utils

* apis-override-select2js

  APIS overrides select2js to be able to provide autocomplete fields that also
  integrate external sources. This package provides the patched Javascript
  files - it has to be listed in ``INSTALLED_APPS`` *before*
  ``django-autocomplete-light`` packages.

* crispy-bootstrap4

  The default theme used for the crispy forms

* django-simple-history

  Used by ``apis_core.history`` to implement version tracking.

* pydot

  Used in ``apis_core.documentation`` to create a dot representation of the
  datamodel.
