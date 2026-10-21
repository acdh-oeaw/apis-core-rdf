from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView

from .forms import UriCreateFromObjectForm
from .models import Uri


class UriCreateView(FormView):
    template_name = "uris/uri_create_view.html"
    form_class = UriCreateFromObjectForm

    def setup(self, *args, **kwargs):
        self.contenttype = get_object_or_404(
            ContentType, app_label=kwargs["app_label"], model=kwargs["model"]
        )
        super().setup(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object"] = get_object_or_404(
            self.contenttype.model_class(), pk=self.kwargs.get("pk")
        )
        return ctx

    def form_valid(self, form):
        uri = form.cleaned_data["uri"]
        uri = Uri.objects.get_or_create(
            uri=uri, content_type=self.contenttype, object_id=self.kwargs.get("pk")
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path + "?success"
