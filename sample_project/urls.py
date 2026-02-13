from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path("", include("apis_core.urls", namespace="apis")),
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#module-django.contrib.auth.views
    path("accounts/", include("django.contrib.auth.urls")),
    # https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#hooking-adminsite-to-urlconf
    path("admin/", admin.site.urls),
    path(
        'jsi18n/',
        cache_page(3600)(JavaScriptCatalog.as_view(packages=['formset'])),
        name='javascript-catalog'
    ),
]
