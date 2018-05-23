from django.test import TestCase
from model_mommy import mommy

from ..models import Weapon


class TestModels(TestCase):
    """
    Test Weapon model.
    """

    def setUp(self):
        """
        Create items.
        """
        for _ in range(5):
            mommy.make(Weapon)

    def tearDown(self):
        """
        Destroy items.
        """
        Weapon.objects.all().delete()

    def test_weapon_exists(self):
        """Validate weapon created."""
        self.assertTrue(Weapon.objects.count() == 5)
