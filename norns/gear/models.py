from django.db import models

from room.models import Tile


class Weapon(models.Model):
    """
    Weapon model.
    """

    name = models.CharField(max_length=255, default='Untitled')
    strength = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    tiles = models.ManyToManyField(
        Tile, related_name='weapons', blank=True)


class Inventory(models.Model):
    """
    Inventory model.
    """

    weapons = models.ManyToManyField(
        Weapon, related_name='inventories', blank=True)
