from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView

from apis_core.profile.models import Bookmark


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"


class ToggleBookmark(LoginRequiredMixin, TemplateView):
    template_name = "toggle_bookmark.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        content_type = ContentType.objects.get(pk=kwargs["content_type_id"])
        bookmark, created = Bookmark.objects.get_or_create(content_type=content_type, object_id=kwargs["object_id"], user=self.request.user)
        if not created:
            bookmark.delete()
        context["exists"] = not created
        context["content_type_id"] = kwargs["content_type_id"]
        context["object_id"] = kwargs["object_id"]
        return context

