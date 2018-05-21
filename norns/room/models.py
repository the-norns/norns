from django.db import models


class Room(models.Model):
    """Room model."""
    room_north = models.ForeignKey(
        'self',
        blank=True,
        related_name='to_south',
        on_delete=models.CASCADE,
    )
    room_east = models.ForeignKey(
        'self',
        blank=True,
        related_name='to_west',
        on_delete=models.CASCADE,
    )
    room_south = models.ForeignKey(
        'self',
        blank=True,
        related_name='to_north',
        on_delete=models.CASCADE,
    )
    room_west = models.ForeignKey(
        'self',
        blank=True,
        related_name='to_east',
        on_delete=models.CASCADE,
    )


class Tile(models.Model):
    """Tile model."""
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
