import os
from django.core.management.utils import get_random_secret_key

SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "apis_override_select2js",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apis_core.core",
    "apis_core.apis_metainfo",
    "apis_core.apis_relations",
    "apis_core.apis_entities",
    "apis_core.apis_vocabularies",
    "apis_core.generic",
    "apis_core.collections",
    "apis_core.history",
    # ui stuff
    "crispy_forms",
    "crispy_bootstrap4",
    "django_filters",
    "django_tables2",
    "dal",
    "dal_select2",
    # api
    "rest_framework",
    # for swagger ui generation
    "drf_spectacular",
    # our ontology
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
