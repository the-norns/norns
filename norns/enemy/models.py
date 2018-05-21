from django.db import models
from status.models import Ability
from get.models import Weapon
from room.models import Tile


class Enemy(models.Model):
    """Enemy model."""
    name = models.CharField()
    abilities = models.ManyToManyField(Ability, blank=True)
    loot = models.ForeignKey(Weapon, blank=True)
    tiles = models.ManyToManyField(Tile, related_name='enemies', blank=True)
