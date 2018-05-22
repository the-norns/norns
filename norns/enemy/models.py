from django.db import models
from status.models import Ability
from gear.models import Weapon
from room.models import Tile


class Enemy(models.Model):
    """Enemy model."""
    name = models.CharField(max_length=255, default='Unnamed')
    abilities = models.ManyToManyField(Ability, blank=True)
    loot = models.ForeignKey(
        Weapon, blank=True, on_delete=models.CASCADE, null=True)
    tiles = models.ManyToManyField(
        Tile, related_name='enemies', blank=True)
