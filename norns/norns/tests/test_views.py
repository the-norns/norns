from django.test import TestCase

from ..views import AboutView, HomeView, StoreView


class TestViews(TestCase):
    """
    Test views.
    """

    def test_valid_view(self):
        """
        Use import.
        """
        self.assertIsNotNone(AboutView.as_view())
        self.assertIsNotNone(HomeView.as_view())
        self.assertIsNotNone(StoreView.as_view())
