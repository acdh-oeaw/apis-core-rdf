import dj_database_url

from .base import *
import sys


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APIS_BASE_URI = "https://apis.acdh.oeaw.ac.at/"

ALLOWED_HOSTS = []

SECRET_KEY = 'd3j@454545()(/)@zlck/6dsaf*#sdfsaf*#sadflj/6dsfk-11$)d6ixcvjsdfsdf&-u35#ayi'
DEBUG = True
DEV_VERSION = False

INSTALLED_APPS += ['gm2m', 'apis_highlighter']

DATABASES = {}

DATABASES['default'] = dj_database_url.config(conn_max_age=600)


LANGUAGE_CODE = "de"

APIS_RELATIONS_FILTER_EXCLUDE += ['annotation', 'annotation_set_relation']
