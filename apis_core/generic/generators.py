from django.contrib.contenttypes.models import ContentType
from django.urls import resolve, reverse
from drf_spectacular.generators import EndpointEnumerator, SchemaGenerator

from apis_core.generic.abc import GenericModel

# Custom Schema Generator
#
# The CustomSchemaGenerator is meant as a drop in replacement for the
# "DEFAULT_GENERATOR_CLASS" of drf-spectacular. You can use it like this:
# SPECTACULAR_SETTINGS["DEFAULT_GENERATOR_CLASS"] = 'apis_core.generic.generators.CustomSchemaGenerator'
#
# Reasons:
# The first reason is, that we are using a custom converter
# (`apis_core.generic.urls.ContenttypeConverter`) to provide access to views
# and api views of different contenttypes. The default endpoint generator of
# does not know about this converter and therefore sees the endpoints using
# this converter as *one* endpoint with one parameter called `contenttype`.
# Thats not what we want, so we have to do our own enumeration - we iterate
# through all contenttypes that inherit from `GenericModel` and create
# schema endpoints for those programatically.
# The second reason is, that the autoapi schema generator of DRF Spectacular
# and our `apis_core.generic.api_views.ModelViewSet` don't work well together.
# Our ModelViewSet needs the dispatch method to set the model of the
# `ModelViewSet`, but this method is not being called by the generator while
# doing the inspection, which means the `ModelViewSet` does not know about the
# model it should work with and can not provide the correct serializer and filter
# classes. Therefore we create the callback for the endpoints by hand and set
# the model from there.


class CustomEndpointEnumerator(EndpointEnumerator):
    def _generate_content_type_endpoint(
        self, content_type: ContentType, method: str = "list"
    ):
        """Create a endpoint tuple, usable by the SchemaGenerator of DRF spectacular"""
        path = reverse("apis_core:generic:genericmodelapi-list", args=[content_type])
        cls = resolve(path).func.cls

        if method == "detail":
            path += "{id}/"
        regex = path
        # for now we only do "GET"
        httpmethod = "GET"
        # we have to add a attribute, so that the
        # `initkwargs` argument to the `as_view`
        # method can contain a `model` argument
        cls.model = None
        callback = cls.as_view({"get": method}, model=content_type.model_class())
        return (path, regex, httpmethod, callback)

    def get_api_endpoints(self, patterns=None, prefix=""):
        """
        Call the EndpointEnumerator's `get_api_endpoints` method to get all
        the automatically found endpoints, remove the ones that we want to override
        and the add our custom endpoints to this list.
        """
        api_endpoints = super().get_api_endpoints(patterns, prefix)
        api_endpoints = [
            endpoint
            for endpoint in api_endpoints
            if not endpoint[0].startswith("/apis/api/{contenttype}/")
        ]
        for content_type in ContentType.objects.all():
            if content_type.model_class() is not None and issubclass(
                content_type.model_class(), GenericModel
            ):
                api_endpoints.append(self._generate_content_type_endpoint(content_type))
                api_endpoints.append(
                    self._generate_content_type_endpoint(content_type, "detail")
                )
        return api_endpoints


class CustomSchemaGenerator(SchemaGenerator):
    endpoint_inspector_cls = CustomEndpointEnumerator
