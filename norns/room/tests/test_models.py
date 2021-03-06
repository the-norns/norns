from django.test import TestCase
from model_mommy import mommy

from ..models import Room, Tile


class TestModels(TestCase):
    """
    Test Room and Tile models.
    """

    def setUp(self):
        """
        Create test room.
        """
        self.room = mommy.make(Room)
        Tile.objects.all().delete()
        self.room.tile_set.set([])
        self.tile1 = mommy.make(Tile, room=self.room)
        self.tile2 = mommy.make(Tile, room=self.room)

    def tearDown(self):
        """
        Destroy test room.
        """
        Room.objects.all().delete()

    def test_room_exists(self):
        """Validate room created."""
        self.assertEqual(Room.objects.count(), 1)

    def test_tile_exists(self):
        """Validate tile created."""
        self.assertGreaterEqual(Tile.objects.count(), 2)

    def test_room_has_tiles(self):
        """Validate room has tiles."""
        self.assertGreaterEqual(self.room.tile_set.count(), 2)

    def test_tile_has_room(self):
        """Validate tiles have room."""
        self.assertIs(self.tile1.room, self.room)
        self.assertIs(self.tile2.room, self.room)


class TestModelsWithData(TestCase):
    """
    Test Room and Tile models.
    """

    fixtures = ['status/fixtures/fixture.json', 'fixture']

    def setUp(self):
        """
        Create room models.
        """
        self.room = mommy.make(Room)

    def tearDown(self):
        """
        Destroy room models.
        """
        Room.objects.all().delete()

    def test_room_has_tiles(self):
        """
        Validate room has tiles.
        """
        self.assertEqual(self.room.tile_set.count(), self.room.grid_size ** 2)

    def test_tiles_can_reveal(self):
        """
        Validate tiles look.
        """
        for tile in self.room.tile_set.all():
            self.assertFalse(tile.looked)
            tile.look()
            self.assertTrue(tile.looked)
