from django.test import TestCase
from model_mommy import mommy

from enemy.models import Enemy
from player.models import Player
from room.models import Room

from ..models import Ability


class TestModelsAbility(TestCase):
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
        room = self.player.tile.room
        self.enemy = mommy.make(Enemy, tile=self.player.tile)
        mommy.make(Room, room_north=room)
        mommy.make(Room, room_south=room)
        mommy.make(Room, room_east=room)
        mommy.make(Room, room_west=room)

    def tearDown(self):
        """
        Destroy items.
        """
        Enemy.objects.all().delete()
        Player.objects.all().delete()

    def test_run_safe(self):
        """
        Test ability to use actions.
        """
        safe = Ability.objects.filter(action='SR').first()
        self.assertEqual(safe.use_ability(self.player, None), 'You used Safe')
        self.assertIsNone(Enemy.objects.filter(pk=self.enemy.pk).first())

    def test_run_safe_room_north(self):
        """
        Test ability to use actions.
        """
        safe = Ability.objects.filter(action='SR').first()
        self.enemy.tile = (
            self.player.tile.room.room_north.tile_set.order_by('?').first())
        self.assertEqual(safe.use_ability(self.player, None), 'You used Safe')
        self.assertIsNone(Enemy.objects.filter(pk=self.enemy.pk).first())

    def test_run_out_of_room(self):
        """
        Test ability to use actions.
        """
        ability = Ability.objects.order_by('?').first()
        self.enemy.tile = (
            self.player.tile.room.room_east.tile_set.order_by('?').first())
        self.assertEqual(
            ability.use_ability(self.player, self.enemy),
            'No target found.')


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
