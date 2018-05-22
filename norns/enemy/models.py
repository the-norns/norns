from django.db import models

from gear.models import Weapon, Inventory
from room.models import Tile
from status.models import Ability


class Enemy(models.Model):
    """
    Enemy model.
    """

    name = models.CharField(max_length=255, default='Unnamed')
    health = models.IntegerField(default=10)
    abilities = models.ManyToManyField(Ability, blank=True)
    inventory = models.ForeignKey(
        Inventory,
        blank=True,
        related_name='enemies',
        on_delete=models.CASCADE,
        null=True)
    weapon = models.ForeignKey(
        Weapon,
        blank=True,
        related_name='enemies',
        on_delete=models.CASCADE,
        null=True)
    tiles = models.ManyToManyField(
        Tile, related_name='enemies', blank=True)
