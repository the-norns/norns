from django.test import TestCase

from ..views import about_view, HomeView, StoreView


class TestViews(TestCase):
    """
    Test views.
    """

    def test_valid_view(self):
        """
        Use import.
        """
        self.assertIsNotNone(about_view)
        self.assertIsNotNone(HomeView.as_view())
        self.assertIsNotNone(StoreView.as_view())
