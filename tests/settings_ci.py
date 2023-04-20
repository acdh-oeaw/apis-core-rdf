SECRET_KEY = "a+nkut46lzzg_=ul)zrs29$u_6^*)2by2mjmwn)tqlgw)_at&l"
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apis_core.apis_metainfo",
    "apis_core.apis_vocabularies",
    "apis_core.apis_relations",
    "apis_core.apis_entities",
    "reversion",
    # ui stuff
    "crispy_forms",
    "django_filters",
    "django_tables2",
    "dal",
    "dal_select2",
    # api
    "rest_framework",
    "rest_framework.authtoken",
    # for swagger ui generation
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allow_cidr.middleware.AllowCIDRMiddleware",
    "reversion.middleware.RevisionMiddleware",
]

ROOT_URLCONF = "apis_core.urls"

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
                # we need this for accessing `basetemplate`
                "apis_core.context_processors.custom_context_processors.list_apis_settings",
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
