from django.test import TestCase

from ..views import WeaponView


class TestViews(TestCase):
    """
    Test views.
    """

    def test_valid_view(self):
        """
        Use import.
        """
        self.assertIsNotNone(WeaponView.as_view())
