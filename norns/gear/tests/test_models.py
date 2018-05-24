from django.db.models import Q
from django.test import TestCase
from model_mommy import mommy

from enemy.models import Enemy
from player.models import Player

from ..models import Consumable, Weapon


class TestModels(TestCase):
    """
    Test Weapon model.
    """

    fixtures = [
            'status/fixtures/fixture.json',
            'fixture',
    ]

    def setUp(self):
        """
        Create items.
        """
        self.player = mommy.make(Player)
        self.enemy = mommy.make(Enemy, tile=self.player.tile)
        self.consumable = Consumable.objects.first()
        self.consumable.tile_set.add(self.player.tile)
        self.weapon = Weapon.objects.first()
        self.weapon.tile_set.add(self.player.tile)

    def tearDown(self):
        """
        Destroy items.
        """
        Weapon.objects.all().delete()

    def test_weapon_exists(self):
        """
        Validate weapon created.
        """
        self.assertTrue(Weapon.objects.count() > 0)

    def test_consumable_loot(self):
        """
        Validate that looted consumable goes in player inventory.
        """
        cinv = self.player.inventory.consumables
        self.assertEqual(cinv.count(), 0)
        self.consumable.loot(self.player)
        self.assertEqual(
            self.consumable.tile_set.filter(id=self.player.tile.id).count(), 0)
        self.assertEqual(
            cinv.filter(id=self.consumable.id).count(), 1)

#    def test_consumable_use(self):
#        """
#        Validate that consumable in inventory is used.
#        """
#        cinv = self.player.inventory.consumables
#        cinv.add(self.consumable)
#        self.consumable.handle_use(self.player, self.enemy)
#        self.assertEqual(cinv.count(), 0)

    def test_weapon_attack_enemy(self):
        """
        Validate that attack attacks enemy target.
        """
        self.enemy.tile = self.player.tile
        initial_health = self.enemy.health
        message = self.weapon.attack(self.player, self.enemy).split()
        damage = int(message[5]) if message[0] == 'Crit!' else int(message[4])
        self.assertEqual(self.enemy.health, initial_health - damage)

    def test_weapon_kill_enemy(self):
        """
        Validate that enough attacks kill enemy target.
        """
        self.enemy.tile = self.player.tile
        while self.enemy.health > 0:
            self.weapon.attack(self.player, self.enemy)
        self.assertIsNone(self.enemy.id)

    def test_weapon_attack_player(self):
        """
        Validate that attack attacks player target.
        """
        self.enemy.tile = self.player.tile
        initial_health = self.player.health
        message = self.weapon.attack(self.enemy, self.player).split()
        damage = int(message[5]) if message[0] == 'Crit!' else int(message[4])
        self.assertEqual(self.player.health, initial_health - damage)

    def test_weapon_kill_player(self):
        """
        Validate that enough attacks kill and relo player.
        """
        self.enemy.tile = self.player.tile
        while self.player.health > 0:
            message = self.weapon.attack(self.enemy, self.player).split()
        self.assertEqual(message[-1], 'died.')

    def test_attack_out_of_range(self):
        """
        Validate that a weapon cannot attack a target out of range.
        """
        tile_set = self.player.tile.room.tile_set
        initial_health = self.enemy.health
        self.player.tile = tile_set.filter(
            Q(x_coord=0) &
            Q(y_coord=0)).first()
        self.enemy.tile = tile_set.filter(
            Q(x_coord=4) &
            Q(y_coord=4)).first()
        message = self.weapon.attack(self.player, self.enemy)
        self.assertEqual(
            message, '{} is out of range.'.format(self.enemy.name))
        self.assertEqual(initial_health, self.enemy.health)
