from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from model_mommy import mommy

from gear.models import Consumable, Weapon
from player.models import Player

from ..models import Room, Tile


class TestRoutes(TestCase):
    """Integration tests."""

    def setUp(self):
        """
        Set up.
        """
        self.user = mommy.make(User)

    def tearDown(self):
        """
        Tear down.
        """
        Player.objects.all().delete()
        Room.objects.all().delete()
        Tile.objects.all().delete()
        Weapon.objects.all().delete()
        Consumable.objects.all().delete()

    def test_new_room_route_makes_new_room(self):
        """
        Validate that new room route creates a new room.
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse_lazy('new_room'))
        self.client.logout()
        self.assertEqual(response.data['message'], 'Welcome to Hel.')
        self.assertTrue(response.data['tiles'][0])


class TestRoutesWithData(TestCase):
    """
    Integration tests.
    """

    fixtures = ['fixture']

    def setUp(self):
        """
        Set up.
        """
        self.user = mommy.make(User)

    def tearDown(self):
        """
        Tear down.
        """
        Player.objects.all().delete()

    def test_look_returns_weapon(self):
        """
        Look at tile for data.

        Validate that looking on a tile returns the weapon on that tile
        and the description on that tile.
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse_lazy('new_room'))
        player = Player.get_active_player(self.user)
        weapon = mommy.make(Weapon, name='sword')
        weapon.save()
        player.tile.desc = 'a tile.'
        player.tile.weapons.add(weapon)
        player.tile.save()
        data = {'user_input': 'look'}
        response = self.client.post(reverse_lazy('room'), data=data)
        self.client.logout()
        self.assertContains(response, 'message')
        self.assertContains(response, 'tiles')
        for tile in response.data['tiles']:
            self.assertIsNotNone(tile)
            self.assertIn('x_coord', tile)
            self.assertIn('y_coord', tile)
            self.assertIn('weapons', tile)
