from django.db import models
from room.models import Tile


class Weapon(models.Model):
    """Weapon model."""
    name = models.CharField(max_length=255)
    strength = models.IntegerField()
    agility = models.IntegerField()
    tiles = models.ManyToManyField(Tile, related_name='weapons', blank=True)
