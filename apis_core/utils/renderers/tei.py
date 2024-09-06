from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from rest_framework import renderers


class TeiRenderer(renderers.BaseRenderer):
    media_type = "text/xml"
    format = "tei"
    template_name = None

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if self.template_name:
            template = loader.get_template(self.template_name)
            request = renderer_context["request"]
            return template.render(data, request=request)
        raise ImproperlyConfigured(
            "Returned a template response with no `template_name` attribute set on the object"
        )
