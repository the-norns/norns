from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

from gear.models import Weapon
from player.models import Player

from ..models import Enemy


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

    def test_enemy_exists(self):
        """
        Validate enemy created.
        """
        self.assertGreaterEqual(Enemy.objects.count(), 1)

    def test_enemy_do_combat_attack(self):
        """
        Validate enemy attacks when in range of player
        """
        self.enemy.tile = self.player.tile
        message = ''
        while message != 'died.':
            message = self.enemy.do_combat().split()[-1]
