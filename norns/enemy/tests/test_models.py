from django.contrib.auth.models import User
from django.db.models import Q
from django.test import TestCase
from model_mommy import mommy

from player.models import Player
from ..models import Enemy
from gear.models import Weapon


class TestModels(TestCase):
    """
    Test Enemy model.
    """

    fixtures = [
        'status/fixtures/fixture.json',
        'fixture',
    ]

    def setUp(self):
        """
        Create enemy models.
        """
        self.user = mommy.make(User)
        self.player = Player.objects.filter(user=self.user).first()
        self.enemy = mommy.make(Enemy)
        self.enemy.weapon = Weapon.objects.first()

    def tearDown(self):
        """
        Destroy enemy models.
        """
        User.objects.all().delete()
        Player.objects.all().delete()
        Enemy.objects.all().delete()

    def test_enemy_exists(self):
        """
        Validate enemy created.
        """
        self.assertGreaterEqual(Enemy.objects.count(), 1)

    def test_enemy_do_combat_attack(self):
        """
        Validate enemy attacks when in range of player.
        """
        self.enemy.tile = self.player.tile
        message = ''
        while message != 'died.':
            message = self.enemy.do_combat().split()[-1]

    def test_enemy_do_combat_approach_player(self):
        """
        Validate enemy approaches then attacks player.
        """
        tl_tile = self.player.tile.room.tile_set.filter(
            Q(x_coord=0) &
            Q(y_coord=0)).first()
        br_tile = self.player.tile.room.tile_set.filter(
            Q(x_coord=self.player.tile.room.grid_size-1) &
            Q(y_coord=self.player.tile.room.grid_size-1)).first()

        self.player.tile = tl_tile
        self.enemy.tile = br_tile
        self.enemy.weapon.reach = 1
        message = ''
        while message != 'died.':
            message = self.enemy.do_combat().split()[-1]
