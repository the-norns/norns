from django.test import TestCase
from ..models import Weapon
from model_mommy import mommy


class TestModels(TestCase):
    """
    Test Weapon model.
    """

    def setUp(self):
        for _ in range(5):
            mommy.make(Weapon)

    def tearDown(self):
        Weapon.objects.all().delete()

    def test_weapon_exists(self):
        """Validate weapon created."""
        self.assertTrue(Weapon.objects.count() == 5)
