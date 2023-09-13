from .base import *

INSTALLED_APPS.remove("webpage")
INSTALLED_APPS.remove("charts")
INSTALLED_APPS.remove("apis_ontology")
INSTALLED_APPS += ["apis_core.relations"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/tmp/db.sqlite3",
    },
}
