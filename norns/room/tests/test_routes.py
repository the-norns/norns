from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from model_mommy import mommy

from player.models import Player
from gear.models import Weapon, Consumable

from ..models import Room, Tile


class TestRoutes(TestCase):
    """Integration tests."""
    def setUp(self):
        self.user = mommy.make(User)

    def tearDown(self):
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
        # import pdb; pdb.set_trace()
        self.assertEqual(response.data['message'], 'Welcome to Hel.')
        self.assertTrue(response.data['tiles'][0]['room'])
