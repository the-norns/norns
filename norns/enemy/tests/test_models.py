from django.test import TestCase
from room.models import Tile
from gear.models import Weapon
from ..models import Enemy
from model_mommy import mommy


class TestModels(TestCase):
    """
    Test Enemy model.
    """

    def setUp(self):
        self.tile1 = mommy.make(Tile)
        self.tile2 = mommy.make(Tile)
        self.loot = mommy.make(Weapon)
        self.enemy = mommy.make(Enemy)
        self.enemy.tiles.add(self.tile1)
        self.enemy.tiles.add(self.tile2)
        self.enemy.loot = self.loot

    def tearDown(self):
        Enemy.objects.all().delete()

    def test_enemy_exists(self):
        """
        Validate enemy created.
        """
        self.assertTrue(Enemy.objects.count() == 1)

    def test_enemy_has_tile(self):
        """
        Validate enemy has a tile.
        """
        self.assertTrue(self.enemy.tiles.count() == 2)

    def test_enemy_has_loot(self):
        """
        Validate enemy has loot.
        """
        self.assertTrue(self.enemy.loot is self.loot)
