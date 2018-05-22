from random import randint

from django.db import models
from django.db.models import Q

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

    def wander(self):
        """
        Possibly move enemy tile.
        """
        rand_x = randint(-1, 1)
        rand_y = randint(-1, 1)
        queryset = Tile.objects.filter(
            Q(y_coord=self.tile.y_coord + rand_y) &
            Q(x_coord=self.tile.x_coord + rand_x) &
            Q(room=self.tile.room))
        if queryset.count():
            self.tile = queryset.first()
