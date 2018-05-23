from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

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
