from random import randint

from django.db import models
from django.dispatch import receiver
from faker import Faker


class EnemyType(models.Model):
    """
    Enemy type model.
    """

    name = models.CharField(max_length=255, default='Unnamed')
    health = models.IntegerField(default=10)


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
    tile = models.ForeignKey('room.Tile', on_delete=models.CASCADE)

    def wander(self):  # pragma: no cover
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

    def move(self, direction):  # pragma: no cover
        """
        Change enemy tile.
        """
        move_direction = {
            'east': self.move_east,
            'north': self.move_north,
            'south': self.move_south,
            'west': self.move_west}.get(direction, None)

        move_direction()
        self.save()

    def move_north(self):  # pragma: no cover
        """
        Change enemy tile north.
        """
        self.tile = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord - 1) &
            models.Q(x_coord=self.tile.x_coord)).first()

    def move_east(self):  # pragma: no cover
        """
        Change enemy tile east.
        """
        self.tile = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord) &
            models.Q(x_coord=self.tile.x_coord + 1)).first()

    def move_south(self):  # pragma: no cover
        """
        Change enemy tile south.
        """
        self.tile = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord + 1) &
            models.Q(x_coord=self.tile.x_coord)).first()

    def move_west(self):  # pragma: no cover
        """
        Change enemy tile west.
        """
        self.tile = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord) &
            models.Q(x_coord=self.tile.x_coord - 1)).first()

    def do_combat(self):
        """
        Attack or advance on player.
        """
        message = ''
        attacked = False
        if self.weapon:
            for tile in self.tile.room.tile_set.all():
                for player in tile.player_set.all():
                    message = self.weapon.attack(self, player)
                    if message.split()[-1] != 'range.':
                        if not self.tile.player_set.count():
                            self.tile.room.round_start = None
                        attacked = True
                        break

            if (
                    not attacked
                    and not self.tile.player_set.count()):  # pragma: no cover
                dist = 5
                min_dx = 5
                min_dy = 5
                for tile in self.tile.room.tile_set.all():
                    for player in tile.player_set.all():
                        dx = self.tile.x_coord - player.tile.x_coord
                        dy = self.tile.y_coord - player.tile.y_coord
                        new_dist = abs(dx) + abs(dy) / 2
                        if new_dist < dist:
                            dist = new_dist
                            min_dx = dx
                            min_dy = dy
                if abs(min_dx) != 0:
                    if min_dx > 0:
                        self.move('west')
                    else:  # pragma: no cover
                        self.move('east')
                else:
                    if min_dy > 0:
                        self.move('north')
                    else:  # pragma: no cover
                        self.move('south')
        return message


@receiver(models.signals.post_save, sender='room.Tile')
def populate_enemies(sender, created=False, instance=None, **kwargs):
    """
    Generate tile mobs.
    """
    fake = Faker()

    if created:
        roll = randint(0, 100)
        if roll > 2:
            return
        Enemy.objects.create(tile=instance, name=fake.first_name())


@receiver(models.signals.pre_save, sender=Enemy)
def populate_enemy_type(sender, instance=None, **kwargs):
    """
    Generate tile mobs.
    """
    if not hasattr(instance, 'enemy_type'):
        if EnemyType.objects.count():
            instance.enemy_type = EnemyType.objects.order_by('?').first()
        else:
            instance.enemy_type = EnemyType.objects.create()
