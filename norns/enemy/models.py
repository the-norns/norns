from random import randint

from django.db import models
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

    enemy_type = models.ForeignKey(EnemyType, on_delete=models.CASCADE)

    abilities = models.ManyToManyField('status.Ability', blank=True)
    inventory = models.OneToOneField(
        'gear.Inventory',
        on_delete=models.CASCADE)
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
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord + rand_y) &
            models.Q(x_coord=self.tile.x_coord + rand_x))
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
        Enemy.objects.create(tile=instance)


@receiver(models.signals.pre_save, sender=Enemy)
def populate_enemy_type(sender, instance=None, **kwargs):
    """
    Generate tile mobs.
    """
    if not instance.enemy_type:
        instance.enemy_type = EnemyType.objects.order_by('?').first()
