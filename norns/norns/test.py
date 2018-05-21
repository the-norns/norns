"""
Core app tests.
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver


class HomeViewUnitTests(TestCase):
    """
    Test for Unit Profile.
    """

    def test_get_home_page(self):
        """
        Test home page.
        """
        response = self.client.get(reverse_lazy('home'))
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')


class LiveServerTests(StaticLiveServerTestCase):
    """
    Test live server rendering.

    fixtures = ['user-data.json']
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize a selenium driver.
        """
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        """
        Destroy a selenium driver.
        """
        cls.selenium.quit()
        del cls.selenium
        super().tearDownClass()

    def test_home(self):
        """
        Test a browser rendering of home page.
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
