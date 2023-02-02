from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from apis_core.apis_entities.api_views import GetEntityGeneric

if "theme" in settings.INSTALLED_APPS:
    urlpatterns = [
        url(r"^apis/", include("apis_core.urls", namespace="apis")),
        url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            r"entity/<int:pk>/", GetEntityGeneric.as_view(), name="GetEntityGenericRoot"
        ),
        url(r"^", include("theme.urls", namespace="theme")),
        url(r"^admin/", admin.site.urls),
        url(r"^info/", include("infos.urls", namespace="info")),
        url(r"^webpage/", include("webpage.urls", namespace="webpage")),
    ]
if "paas_theme" in settings.INSTALLED_APPS:
    urlpatterns = [
        url(r"^apis/", include("apis_core.urls", namespace="apis")),
        url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            r"entity/<int:pk>/", GetEntityGeneric.as_view(), name="GetEntityGenericRoot"
        ),
        url(r"^", include("paas_theme.urls", namespace="theme")),
        url(r"^admin/", admin.site.urls),
        url(r"^info/", include("infos.urls", namespace="info")),
        url(r"^webpage/", include("webpage.urls", namespace="webpage")),
    ]
else:
    urlpatterns = [
        url(r"^apis/", include("apis_core.urls", namespace="apis")),
        url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            r"entity/<int:pk>/", GetEntityGeneric.as_view(), name="GetEntityGenericRoot"
        ),
        url(r"^admin/", admin.site.urls),
        url(r"^info/", include("infos.urls", namespace="info")),
        url(r"^", include("webpage.urls", namespace="webpage")),
    ]


if 'viecpro_vis' in settings.INSTALLED_APPS:
    urlpatterns.insert(0, url(r'^visualisations/', include("viecpro_vis.urls", namespace="viecpro_vis"))
    )
        
if "transkribus" in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + [
        url(r"^transkribus/", include("transkribus.urls")),
    ]

if "apis_bibsonomy" in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r"^bibsonomy/", include("apis_bibsonomy.urls", namespace="bibsonomy"))
    )

if "oebl_irs_workflow" in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(
            r"^workflow/",
            include("oebl_irs_workflow.urls", namespace="oebl_irs_workflow"),
        )
    )
handler404 = "webpage.views.handler404"
