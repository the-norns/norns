from random import randint

from django.db import models
from django.dispatch import receiver


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

    def move(self, direction):
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

    def move_north(self):
        """
        Change enemy tile north.
        """
        self.tile = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord - 1) &
            models.Q(x_coord=self.tile.x_coord)).first()

    def move_east(self):
        """
        Change enemy tile east.
        """
        self.tile = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord) &
            models.Q(x_coord=self.tile.x_coord + 1)).first()

    def move_south(self):
        """
        Change enemy tile south.
        """
        self.tile = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord + 1) &
            models.Q(x_coord=self.tile.x_coord)).first()

    def move_west(self):
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
            for player in self.tile.player_set.all():
                if self.weapon.check_reach(self, player):
                    message = self.weapon.attack(self, player)
                    if not self.tile.player_set.count():
                        self.tile.room.round_start = None
                    attacked = True
                    break

            if not attacked and not self.tile.player_set.count():
                dist = 5
                for player in self.tile.player_set.all():
                    dx = self.tile.x_coord - player.tile.x_coord
                    dy = self.tile.y_coord - player.tile.y_coord
                    new_dist = abs(dx) + abs(dy) / 2
                    if new_dist < dist:
                        if abs(dx) > abs(dy):
                            if dx > 0:
                                self.move('west')
                            else:
                                self.move('east')
                        else:
                            if dy > 0:
                                self.move('north')
                            else:
                                self.move('south')
        return message


@receiver(models.signals.post_save, sender='room.Tile')
def populate_enemies(sender, created=False, instance=None, **kwargs):
    """
    Generate tile mobs.
    """
    if created:
        roll = randint(0, 100)
        if roll > 2:
            return
        Enemy.objects.create(tile=instance)


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
