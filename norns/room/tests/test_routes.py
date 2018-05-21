from django.test import TestCase
from django.urls import reverse_lazy
from gear.models import Weapon
from ..models import Room, Tile
from model_mommy import mommy


class TestRoutes(TestCase):
    """Integration tests."""
    def setUp(self):
        self.room = mommy.make(Room)
        self.tile = mommy.make(Tile, room=self.room, desc='a tile.')
        self.weapon = mommy.make(Weapon, name='sword')
        self.weapon.tiles.add(self.tile)
        self.weapon.save()

    def tearDown(self):
        Room.objects.all().delete()
        Tile.objects.all().delete()
        Weapon.objects.all().delete()

    def test_look_returns_weapon(self):
        """
        Validate that looking on a tile returns the weapon on that tile
        and the description on that tile.
        """
        data = {'verb': 'look', 'tile_id': self.tile.id}
        # import pdb; pdb.set_trace()
        response = self.client.post(
            reverse_lazy('room', args=[self.room.id]), data=data)
        import pdb; pdb.set_trace()
        self.assertContains(response, 'a tile.')
        self.assertContains(response, 'sword')
