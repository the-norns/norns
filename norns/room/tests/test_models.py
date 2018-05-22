from django.test import TestCase
from ..models import Room, Tile
from model_mommy import mommy


class TestModels(TestCase):
    """
    Test Room and Tile models.
    """

    def setUp(self):
        self.room = mommy.make(Room)
        self.tile1 = mommy.make(Tile, room=self.room)
        self.tile2 = mommy.make(Tile, room=self.room)

    def tearDown(self):
        Room.objects.all().delete()

    def test_room_exists(self):
        """Validate room created."""
        self.assertTrue(Room.objects.count() == 1)

    def test_tile_exists(self):
        """Validate tile created."""
        self.assertTrue(Tile.objects.count() == 2)

    def test_room_has_tiles(self):
        """Validate room has tiles."""
        self.assertTrue(self.room.tiles.count() == 2)

    def test_tile_has_room(self):
        """Validate tiles have room."""
        self.assertTrue(self.tile1.room is self.room)
        self.assertTrue(self.tile2.room is self.room)
