from django.db import models
from status.models import Ability
from gear.models import Weapon
from room.models import Tile


class Player(models.Model):
    """Player model."""
    name = models.CharField()
    abilities = models.ManyToManyField(Ability, blank=True)
    weapon = models.ForeignKey(Weapon, blank=True)
    tile = models.ForeignKey(Tile, blank=True)
