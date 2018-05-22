from django.contrib.auth.models import User
from django.db import models
from status.models import Ability
from gear.models import Weapon
from room.models import Tile


class Player(models.Model):
    """Player model."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, default='Unnamed')
    abilities = models.ManyToManyField(Ability, blank=True)
    weapon = models.ForeignKey(
        Weapon, blank=True, on_delete=models.CASCADE, null=True)
    tile = models.ForeignKey(
        Tile, blank=True, on_delete=models.CASCADE, null=True)
