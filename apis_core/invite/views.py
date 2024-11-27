from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView

from apis_core.invite.models import InviteToken


class Invite(CreateView):
    form_class = UserCreationForm
    template_name = "invite.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.invite = get_object_or_404(InviteToken, id=kwargs.get("invite"))

    def form_valid(self, form):
        ret = super().form_valid(form)
        self.invite.delete()
        messages.success(self.request, f"Created user {self.object}")
        return ret

    def get_success_url(self):
        return reverse("apis_core:login")
