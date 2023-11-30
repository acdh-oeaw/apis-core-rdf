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
* PyYAML
* rdflib
* drf-spectacular
* requests
* SPARQLWrapper
* django-model-utils
* pandas
* django-admin-csvexport

  Used in the ``apis_labels`` and ``apis_vocabularies`` admin apps

* tablib

  `You must have tablib installed in order to use the django-tables2 export functionality` - 
  the export functionality is used in the entities list view.

* setuptools

  ``django-model-utils`` uses this, see https://github.com/jazzband/django-model-utils/issues/568
