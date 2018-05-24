from django.test import TestCase
from model_mommy import mommy

from enemy.models import Enemy
from player.models import Player

from ..models import Ability


class TestModels(TestCase):
    """
    Test models.
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

    def tearDown(self):
        """
        Destroy items.
        """
        Enemy.objects.all().delete()
        Player.objects.all().delete()

    def test_run_1(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=1)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_2(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=2)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_3(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=3)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_4(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=4)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_5(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=5)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_6(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=6)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_7(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=7)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_7(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=7)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_8(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=8)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_9(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=9)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_10(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=10)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)

    def test_run_11(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.get(pk=11)
        self.assertIsNotNone(ability)
        ability.use_ability(self.player, self.enemy)
