---
title: Configuration
---

# `APIS_BASE_URI`

When you create an instance of an entity, a signal
[apis_core.apis_entities.models.create_default_uri][] is triggered that tries to generate a canonical URI for
the entity. The signal can be disabled by setting the
`CREATE_DEFAULT_URI` setting to `False`. If the signal runs, it creates
the canonical URI from two parts. The first part comes from the
`APIS_BASE_URI` setting. The second part comes from the reverse route of
`GetEntityGenericRoot` if that exists. If not, it uses the reverse
route of `apis_core:GetEntityGeneric`, which is defined in
[apis_core.urls][] and defaults to
`/entity/{pk}`. If the value of `APIS_BASE_URI` changes and URLs
containing the former `APIS_BASE_URI` remain in the database, then the
old `APIS_BASE_URI` value must be added to the setting
`APIS_FORMER_BASE_URIS`. `APIS_FORMER_BASE_URIS` is a list that contains
base URLs that were once used.

# Django settings

This section deals with the internal configuration of APIS. For
instructions on how to set it up please refer to
[installation](installation.md). All the settings described
here are part of the Django settings and can be set in the `settings.py`
file of your Django project.

## REST_FRAMEWORK

APIS uses [Django
REST framework](https://www.django-rest-framework.org/) for API
provisioning. REST framework-specific settings like the default page size
can be set here.

``` python
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "rest_framework.permissions.DjangoModelPermissions",
)
```

Use the above default for allowing every user with permissions on a
model to change all model instances. Set
`"rest_framework.permissions.IsAuthenticated"` if every logged-in user
should have all permissions.

``` python
REST_FRAMEWORK["PAGE_SIZE"] = 50
```

Sets the default page size the APIS REST API should deliver.

## SPECTACULAR_SETTINGS

We provide a custom schema generator for spectacular. It is meant as a
drop in replacement for the `DEFAULT_GENERATOR_CLASS` of
drf-spectacular. You can use it like this:

``` python
SPECTACULAR_SETTINGS["DEFAULT_GENERATOR_CLASS"] = 'apis_core.generic.generators.CustomSchemaGenerator'
```

Background:

The first reason is that we are using a custom converter
([apis_core.generic.urls.ContenttypeConverter][]) to provide access to views and API views of different
content types. The default endpoint generator of drf-spectacular does
not know about this converter and therefore sees the endpoints using
this converter as *one* endpoint with one parameter called
`contenttype`. That is not what we want, so we have to do our own
enumeration: we iterate through all content types that inherit from
`GenericModel` and create schema endpoints for those programmatically.

The second reason is that the `autoapi` schema generator of DRF
Spectacular and our
[apis_core.generic.api_views.ModelViewSet][] don't work well together. Our ModelViewSet needs the
dispatch method to set the model of the `ModelViewSet`, but this method
is not being called by the generator while doing the inspection, which
means the `ModelViewSet` does not know about the model it should work
with and can not provide the correct serializer and filter classes.
Therefore, we create the callback for the endpoints by hand and set the
model from there.

## APIS_BASE_URI

``` python
APIS_BASE_URI = "https://your-url-goes-here.com"
```

Sets the base URI your instance should use. This is important as APIS
uses mainly URIs instead of IDs. This setting is used to generate the
canonical URI of an entity. It is included in the serializations of
entities (for example the JSON returned by the API) and therefore should be set
to the URL your production app is running on.

## APIS_NEXT_PREV

``` python
APIS_NEXT_PREV = True
```

## APIS_ANON_VIEWS_ALLOWED

``` python
APIS_ANON_VIEWS_ALLOWED = False
```

Sets whether list and detail views are accessible for anonymous (not
logged-in) users. If only a subset of the data should be exposed to the
anonymous user, use [custom
managers](https://docs.djangoproject.com/en/stable/topics/db/managers/#custom-managers).

## Maintenance middleware

APIS ships a maintenance middleware that you can use and activate to
enable a maintenance mode in your project. Maintenance mode means that
only superuser accounts can access the web interfaces; all other requests
are being answered with a simple maintenance mode page (the
`maintenance.html` template). To use the middleware, add

``` python
"apis_core.core.middleware.MaintenanceMiddleware"
```

to your `settings.MIDDLEWARE` list. To activate the maintenance mode
once the middleware is enabled, simply create a file `apis_maintenance`
in the directory the main Django process runs in. The path of the
maintenance file can be changed in settings:
`APIS_MAINTENANCE_FILE = "path of the file"`
