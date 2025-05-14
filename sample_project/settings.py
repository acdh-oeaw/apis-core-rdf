import os

from django.core.management.utils import get_random_secret_key

SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())
DEBUG = True

# we look for values in the environment and fallback to the
# Django defaults if there are none set
env_ah = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = list(filter(None, env_ah))
env_csrf = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
CSRF_TRUSTED_ORIGINS = list(filter(None, env_csrf))


# Application definition

INSTALLED_APPS = [
    # our main app, containing the ontology (in the `models.py`)
    # and our customizations
    "sample_project",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ui stuff used by APIS
    "crispy_forms",
    "crispy_bootstrap4",
    "crispy_bootstrap5",
    "django_filters",
    "django_tables2",
    "dal",
    "dal_select2",
    # REST API
    "rest_framework",
    # swagger ui generation
    "drf_spectacular",
    # The APIS apps
    "apis_core.generic",
    # APIS collections provide a collection model similar to
    # SKOS collections and allow tagging of content
    "apis_core.collections",
    "apis_core.apis_metainfo",
    "apis_core.relations",
    "apis_core.history",
    "apis_core.apis_entities",
    # APIS history modules tracks changes of instances over
    # time and lets you revert changes
    # The core APIS apps come last, so other apps can override
    # and extend their templates
    "apis_core.core",
    "apis_core.documentation",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "crum.CurrentRequestUserMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/tmp/db.sqlite3",
    },
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5.html"

# for django spectacular to be able to generate the schema, we have to use its view inspector
REST_FRAMEWORK = {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"}
# we use our custom schema generator to make it pick up our custom routes
SPECTACULAR_SETTINGS = {
    "DEFAULT_GENERATOR_CLASS": "apis_core.generic.generators.CustomSchemaGenerator"
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-6s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
