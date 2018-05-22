from random import randint

from django.db import models
from django.db.models import Q
from django.dispatch import receiver


class EnemyType(models.Model):
    """
    Enemy type model.
    """

    name = models.CharField(max_length=255, default='Unnamed')


class Enemy(models.Model):
    """
    Enemy model.
    """

    name = models.CharField(max_length=255, default='Unnamed')
    health = models.IntegerField(default=10)

    enemy_type = models.ForeignKey(
        EnemyType, on_delete=models.CASCADE, null=True)

    abilities = models.ManyToManyField('status.Ability', blank=True)
    inventory = models.OneToOneField(
        'gear.Inventory',
        blank=True,
        on_delete=models.CASCADE,
        null=True)
    weapon = models.ForeignKey(
        'gear.Weapon',
        blank=True,
        on_delete=models.SET_NULL,
        null=True)
    tile = models.ForeignKey(
        'room.Tile', blank=True, on_delete=models.SET_NULL, null=True)

    def wander(self):
        """
        Possibly move enemy tile.
        """
        rand_x = randint(-1, 1)
        rand_y = randint(-1, 1)
        queryset = self.tile.room.tiles.filter(
            Q(y_coord=self.tile.y_coord + rand_y) &
            Q(x_coord=self.tile.x_coord + rand_x))
        if queryset.count():
            self.tile = queryset.first()


@receiver(models.signals.post_save, sender='room.Tile')
def populate_enemies(sender, created=False, instance=None, **kwargs):
    """
    Generate tile mobs.
    """
    if created:
        roll = randint(0, 10)
        if roll > 2:
            return
        Enemy(
            enemy_type=EnemyType.order_by('?').first(),
            tile=instance).save()
