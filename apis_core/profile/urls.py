from django.urls import path
from rest_framework import routers

from . import views
from . import api_views

router = routers.DefaultRouter()
router.register(r"", api_views.BookmarkViewSet)

urlpatterns = [
        path("", views.ProfileView.as_view()),
        path("togglebookmark/<int:content_type_id>/<int:object_id>", views.ToggleBookmark.as_view(), name="togglebookmark")
]
