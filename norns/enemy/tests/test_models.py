from django.test import TestCase
from model_mommy import mommy

from gear.models import Weapon
from room.models import Tile

from ..models import Enemy


class TestModels(TestCase):
    """
    Test Enemy model.
    """

    def setUp(self):
        """
        Create enemy models.
        """
        self.tile1 = mommy.make(Tile)
        self.tile2 = mommy.make(Tile)
        Enemy.objects.all().delete()
        Weapon.objects.all().delete()
        self.loot = mommy.make(Weapon)
        self.enemy1 = mommy.make(Enemy)
        self.enemy2 = mommy.make(Enemy)
        self.enemy1.tile = self.tile1
        self.enemy2.tile = self.tile2
        self.enemy1.loot = self.loot

    def tearDown(self):
        """
        Destroy enemy models.
        """
        Enemy.objects.all().delete()

    def test_enemy_exists(self):
        """
        Validate enemy created.
        """
        self.assertEqual(Enemy.objects.count(), 2)

    def test_enemy_has_tile(self):
        """
        Validate enemy has a tile.
        """
        self.assertEqual(self.enemy1.tile, self.tile1)

    def test_enemy_has_loot(self):
        """
        Validate enemy has loot.
        """
        self.assertEqual(self.enemy1.loot, self.loot)
