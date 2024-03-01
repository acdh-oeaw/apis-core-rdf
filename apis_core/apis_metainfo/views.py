from django.views.generic.edit import FormView

from .forms import UriGetOrCreateForm


class UriGetOrCreate(FormView):
    template_name = "uri_create.html"
    form_class = UriGetOrCreateForm

    def form_valid(self, form):
        if form.is_valid():
            self.success_url = form.uriobj.root_object.get_absolute_url()
        return super().form_valid(form)
