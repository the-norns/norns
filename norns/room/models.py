from django.db import models


class Room(models.Model):
    """Room model."""
    room_north = models.ForeignKey('self', blank=True)
    room_east = models.ForeignKey('self', blank=True)
    room_south = models.ForeignKey('self', blank=True)
    room_west = models.ForeignKey('self', blank=True)


class Tile(models.Model):
    """Tile model."""
    room = models.ForeignKey(Room)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
