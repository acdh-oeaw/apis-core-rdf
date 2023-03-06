from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse

from apis_core.apis_metainfo.models import Text, Collection
from reversion import revisions as reversion

from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import Permission



class PermissionsModelTestCase(TestCase):
    name = "test name"
    first_name = "test first name"
    text = "kjhkjsdhaslkdhadh lasdjalsk alsjdhaksjdh"
    col_name = "Test collection"
    start_date = "1.3.1930"
    end_date = "4.6.1960"

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.txt = Text.objects.create(text=cls.text)
        cls.col = Collection.objects.create(name=cls.col_name)
        cls.user = User.objects.create_user("testuser", "apisdev16")
        pe = Permission.objects.get(name="Can change person")
        cls.user.user_permissions.add(pe)
        cls.token = Token.objects.create(user=cls.user).key
        cls.group = Group.objects.create(name="testgroup")
        cls.col.groups_allowed.add(cls.group)
        cls.user.groups.add(cls.group)
        cls.c = APIClient()
        cls.c.credentials(HTTP_AUTHORIZATION="Token " + cls.token)