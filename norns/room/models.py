from django.db import models
from player.models import Player
from enemy.models import Enemy
from gear.models import Weapon


class Room(models.Model):
    """Room model."""
    room_north = models.ForeignKey('self')
    room_east = models.ForeignKey('self')
    room_south = models.ForeignKey('self')
    room_west = models.ForeignKey('self')


class Tile(models.Model):
    """Tile model."""
    room = models.ForeignKey('Room')
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    players = models.ManyToManyField(
        'Player', related_name='tiles', blank=True)
    enemies = models.ManyToManyField(
        'Enemy', related_name='tiles', blank=True)
    weapons = models.ManyToManyField(
        'Weapon', related_name='tiles', blank=True)
