Development
===========

Dependencies
------------

* Django
* djangorestframework
* django-filter
* django-autocomplete-light
* django-cors-headers
* django-crum
* django-crispy-forms
* django-gm2m
* django-leaflet
* django-reversion
* django-tables2
* djangorestframework-csv
* djangorestframework-xml
* rdflib
* drf-spectacular
* requests
* SPARQLWrapper
* django-model-utils
* django-admin-csvexport

  Used in the ``apis_labels`` and ``apis_vocabularies`` admin apps

* tablib

  `You must have tablib installed in order to use the django-tables2 export functionality` - 
  the export functionality is used in the entities list view.

* apis-override-select2js

  APIS overrides select2js to be able to provide autocomplete fields that also
  integrate external sources. This package provides the patched Javascript
  files - it has to be listed in ``INSTALLED_APPS`` *before*
  ``django-autocomplete-light`` packages.

* python-dateutil
  
  Used in ``apis_entities.autocomplete3``
