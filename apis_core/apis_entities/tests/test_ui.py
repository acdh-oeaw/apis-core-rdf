import os
import re

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import Page, expect, sync_playwright


class UITests(StaticLiveServerTestCase):
    fixtures = ["sample_project/fixtures/sample_project.json"]

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=False)
        cls.context = cls.browser.new_context()
        cls.context.tracing.start(screenshots=True, snapshots=True, sources=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.context.tracing.stop(path="trace.zip")
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self) -> None:
        User.objects.create_superuser(
            "mytestuser",
            "mytestuser@test.com",
            "mytestpassword",
            is_staff=True,
        )
        return super().setUp()

    def test_admin_login(self) -> Page:
        page = self.context.new_page()
        page.goto(f"{self.live_server_url}/admin/")
        page.get_by_label("Username:").click()
        page.get_by_label("Username:").fill("mytestuser")
        page.get_by_label("Username:").press("Tab")
        page.get_by_label("Password:").fill("mytestpassword")
        page.get_by_label("Password:").press("Tab")
        page.get_by_role("button", name="Log in").press("Enter")
        return page

    def test_main_menu(self):
        page = self.context.new_page()
        page.goto(self.live_server_url)
        expect(page.get_by_role("button", name="Entities")).to_be_visible()
        expect(page.get_by_role("button", name="Relations")).to_be_visible()
        expect(page.get_by_role("button", name="Collections")).to_be_visible()
        page.get_by_role("button", name="Entities").click()
        expect(page.get_by_role("link", name="Groups")).to_be_visible()
        expect(page.get_by_role("link", name="Persons")).to_be_visible()
        expect(page.get_by_role("link", name="Places")).to_be_visible()
        page.get_by_role("button", name="Relations").click()
        expect(page.get_by_role("link", name="is cousin of")).to_be_visible()
        expect(page.get_by_role("link", name="is siblling of")).to_be_visible()
        expect(page.get_by_role("link", name="lives in")).to_be_visible()
        return page
