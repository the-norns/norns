from random import randint

from django.db import models

import gear
import enemy


class Room(models.Model):
    """
    Room model.
    """

    room_north = models.ForeignKey(
        'self',
        blank=True,
        related_name='to_south',
        on_delete=models.CASCADE,
        null=True,
    )
    room_east = models.ForeignKey(
        'self',
        blank=True,
        related_name='to_west',
        on_delete=models.CASCADE,
        null=True,
    )
    room_south = models.ForeignKey(
        'self',
        blank=True,
        related_name='to_north',
        on_delete=models.CASCADE,
        null=True,
    )
    room_west = models.ForeignKey(
        'self',
        blank=True,
        related_name='to_east',
        on_delete=models.CASCADE,
        null=True,
    )
    grid_size = models.IntegerField(default=5)

    def roll_room(self, direction):
        """
        Create a new room.
        """
        room = Room.create()
        if direction == 'north':
            room.room_south = self
            self.room_north = room
        if direction == 'east':
            room.room_west = self
            self.room_east = room
        if direction == 'south':
            room.room_north = self
            self.room_south = room
        if direction == 'west':
            room.room_east = self
            self.room_west = room

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                tile = Tile.create(x_coord=x, y_coord=y, room=room)
                roll = randint(0, 10)
                if roll == 1:
                    enemy.models.Enemy.order_by('?').first().tiles.add(tile)
        return room


class Tile(models.Model):
    """
    Tile model.
    """

    room = models.ForeignKey(
        Room, related_name='tiles', on_delete=models.CASCADE)
    looked = models.BooleanField(default=False)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    desc = models.TextField(blank=True)

    def roll_tile(self):
        """
        Create disappointment.
        """
        roll = randint(0, 10)
        if roll < 2:
            gear.models.Weapon.order_by('?').first().tiles.add(self)
