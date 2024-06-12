import os
from django.core.management.utils import get_random_secret_key

SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # `apis_override_select2js` is a workaround for APIS'
    # handling of autocomplete forms. It should be listed
    # at the beginning of the list, to make sure the
    # files shipped with it are served in precedence.
    "apis_override_select2js",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ui stuff used by APIS
    "crispy_forms",
    "crispy_bootstrap4",
    "django_filters",
    "django_tables2",
    "dal",
    "dal_select2",
    # REST API
    "rest_framework",
    # swagger ui generation
    "drf_spectacular",
    # The APIS apps
    "apis_core.core",
    "apis_core.generic",
    "apis_core.apis_metainfo",
    "apis_core.apis_relations",
    "apis_core.apis_entities",
    # apis_vocabularies is deprecated, but there are
    # still migrations depending on it - it will be dropped
    # at some point
    "apis_core.apis_vocabularies",
    # APIS collections provide a collection model similar to
    # SKOS collections and allow tagging of content
    "apis_core.collections",
    # APIS history modules tracks changes of instances over
    # time and lets you revert changes
    "apis_core.history",
    # our main app, containing the ontology (in the `models.py`)
    # and our customizations
    "sample_project",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ROOT_URLCONF = "apis_core.urls"
ROOT_URLCONF = "sample_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"
STATIC_ROOT = "/tmp/staticfiles"

PROJECT_DEFAULT_MD = {}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/tmp/db.sqlite3",
    },
}

CRISPY_TEMPLATE_PACK = "bootstrap4"
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"
