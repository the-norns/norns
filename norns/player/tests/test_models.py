from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

from gear.models import Weapon

from ..models import Player


class TestModels(TestCase):
    """
    Test Player model.
    """

    def setUp(self):
        """
        Create player models.
        """
        self.user = mommy.make(User)

    def tearDown(self):
        """
        Destroy player models.
        """
        Player.objects.all().delete()

    def test_player_exists(self):
        """
        Validate player created.
        """
        self.assertGreaterEqual(
            Player.objects.filter(user=self.user).count(), 1)

    def test_player_has_tile(self):
        """
        Validate player created.
        """
        player = Player.objects.filter(user=self.user).first()
        self.assertIsNot(player.tile, None)

    def test_player_can_move_north(self):
        """
        Validate player moves north.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        player.move('north')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)

    def test_player_can_move_south(self):
        """
        Validate player moves south.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        player.move('south')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)

    def test_player_can_move_east(self):
        """
        Validate player moves east.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        player.move('east')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)

    def test_player_can_move_west(self):
        """
        Validate player moves west.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        player.move('west')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)

    def test_player_can_move_north_room(self):
        """
        Validate player moves north.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        while player.tile.room == start.room:
            player.move('north')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)

    def test_player_can_move_south_room(self):
        """
        Validate player moves south.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        while player.tile.room == start.room:
            player.move('south')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)

    def test_player_can_move_east_room(self):
        """
        Validate player moves east.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        while player.tile.room == start.room:
            player.move('east')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)

    def test_player_can_move_west_room(self):
        """
        Validate player moves west.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        while player.tile.room == start.room:
            player.move('west')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)


class TestRoomContinuity(TestCase):
    """
    Test Player model.
    """

    def setUp(self):
        """
        Create player models.
        """
        self.user = mommy.make(User)

    def tearDown(self):
        """
        Destroy player models.
        """
        Player.objects.all().delete()

    def test_player_can_move_north_south(self):
        """
        Validate player moves north south.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        while player.tile.room == start.room:
            player.move('north')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)
        player.move('south')
        self.assertEqual(player.tile.room, start.room)
        while player.tile.room == start.room:
            player.move('south')
        self.assertIsNotNone(player.tile.room)

    def test_player_can_move_south_north(self):
        """
        Validate player moves south north.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        while player.tile.room == start.room:
            player.move('south')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)
        player.move('north')
        self.assertEqual(player.tile.room, start.room)
        while player.tile.room == start.room:
            player.move('north')
        self.assertIsNotNone(player.tile.room)

    def test_player_can_move_east_west(self):
        """
        Validate player moves east west.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        while player.tile.room == start.room:
            player.move('east')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)
        player.move('west')
        self.assertEqual(player.tile.room, start.room)
        while player.tile.room == start.room:
            player.move('west')
        self.assertIsNotNone(player.tile.room)

    def test_player_can_move_west_east(self):
        """
        Validate player moves west east.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        while player.tile.room == start.room:
            player.move('west')
        end = player.tile
        self.assertIsNotNone(end)
        self.assertNotEqual(start, end)
        player.move('east')
        self.assertEqual(player.tile.room, start.room)
        while player.tile.room == start.room:
            player.move('east')
        self.assertIsNotNone(player.tile.room)


class TestModelsWithData(TestCase):
    """
    Test Player model.
    """

    fixtures = ['fixture']

    def setUp(self):
        """
        Create player models.
        """
        self.user = mommy.make(User)

    def tearDown(self):
        """
        Destroy player models.
        """
        Player.objects.all().delete()

    def test_player_action_go(self):
        """
        Validate player moves.
        """
        player = Player.objects.filter(user=self.user).first()
        start = player.tile
        self.assertIsNotNone(start)
        player.handle_user_input('go north'.split())
        self.assertNotEqual(start, player.tile)
        player.handle_user_input('go east'.split())
        self.assertNotEqual(start, player.tile)
        player.handle_user_input('go south'.split())
        self.assertNotEqual(start, player.tile)
        player.handle_user_input('go west'.split())
        end = player.tile
        self.assertIsNotNone(end)
        self.assertEqual(start, end)


class TestPlayerWithInventory(TestCase):
    """
    Test Player model.
    """

    fixtures = ['fixture']

    def setUp(self):
        """
        Create player models.
        """
        self.user = mommy.make(User)
        player = Player.objects.filter(user=self.user).first()
        for _ in range(10):
            weapon = mommy.make(Weapon)
            player.inventory.weapons.add(weapon)

    def tearDown(self):
        """
        Destroy player models.
        """
        Player.objects.all().delete()

    def test_player_action_equip(self):
        """
        Validate player moves.
        """
        player = Player.objects.filter(user=self.user).first()
        weapon = player.weapon
        self.assertIsNone(weapon)
        player.handle_user_input(
            'equip {}'.format(
                player.inventory.weapons.first().name).split())
