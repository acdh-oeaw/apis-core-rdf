"""
URL configuration for sample_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from apis_core.apis_entities.api_views import GetEntityGeneric
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    # APIS refers to the `login` and `logout` urls in its `base.html` template
    # you can define your own or use the ones shipped with Django
    path("accounts/", include("django.contrib.auth.urls")),
    # The APIS views
    path("apis/", include("apis_core.urls", namespace="apis")),
    # It is common for APIS projects to have a shortcut for accessing entities
    path("entity/<int:pk>/", GetEntityGeneric.as_view(), name="GetEntityGenericRoot"),
    path("", TemplateView.as_view(template_name="base.html")),
]

urlpatterns += staticfiles_urlpatterns()
