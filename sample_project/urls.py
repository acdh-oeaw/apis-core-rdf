from django.urls import include, path

urlpatterns = [path("apis/", include("apis_core.urls", namespace="apis"))]
