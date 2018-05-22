from django.db import models

from gear.models import Weapon
from room.models import Tile
from status.models import Ability


class Enemy(models.Model):
    """
    Enemy model.
    """

    name = models.CharField(max_length=255, default='Unnamed')
    abilities = models.ManyToManyField(Ability, blank=True)
    loot = models.ForeignKey(
        Weapon,
        blank=True,
        related_name='enemies',
        on_delete=models.CASCADE,
        null=True)
    tiles = models.ManyToManyField(
        Tile, related_name='enemies', blank=True)
