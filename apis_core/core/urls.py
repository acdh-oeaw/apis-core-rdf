from django.urls import path
from django.views.generic import TemplateView

from apis_core.core.views import Dumpdata

urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html"), name="apis_index"),
    path("api/dumpdata", Dumpdata.as_view()),
]
