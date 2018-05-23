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
        User.objects.create_user(
            username='bob',
            email='bob@bob.com',
        )
        self.user = User.objects.first()
        self.user.password = 'bob'
        self.user.save()
        #import pdb; pdb.set_trace()
        #self.user = mommy.make(User)
        #self.player = mommy.make(Player, user=self.user)
        #weapon = mommy.make(Weapon)
        #player.tile.weapons.add(weapon)

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
        self.assertContains(response.body, 'Welcome to Hel.')
