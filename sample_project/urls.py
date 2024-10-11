from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("apis_core.urls", namespace="apis")),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#module-django.contrib.auth.views
    path("accounts/", include("django.contrib.auth.urls")),
    # https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#hooking-adminsite-to-urlconf
    path("admin/", admin.site.urls),
]
