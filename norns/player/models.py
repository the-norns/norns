from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Player(models.Model):
    """
    Player model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=255, default='Unnamed')
    max_health = models.IntegerField(default=200)
    health = models.IntegerField(default=200)

    abilities = models.ManyToManyField('status.Ability', blank=True)
    inventory = models.OneToOneField(
        'gear.Inventory',
        on_delete=models.CASCADE)
    origin = models.ForeignKey('room.Room', on_delete=models.CASCADE)
    weapon = models.ForeignKey(
        'gear.Weapon',
        blank=True,
        related_name='equiped_set',
        on_delete=models.SET_NULL,
        null=True)
    combat_action = models.CharField(max_length=255, blank=True, null=True)
    tile = models.ForeignKey('room.Tile', on_delete=models.CASCADE)

    def handle_user_input(self, user_input):
        """
        Handle input.
        """

        if not self.tile.room.round_start:
            for tile in self.tile.room.tile_set.all():
                if tile.enemy_set.count():  # pragma: no cover
                    self.tile.room.round_start = datetime.now(timezone.utc)
                    self.tile.room.save()
                    break

        verb = user_input[0]
        if verb == 'go':
            message = self.move(user_input[1])
        elif verb == 'attack':  # pragma: no cover
            target = self.tile.enemy_set.filter(name=user_input[1]).first()
            message = self.weapon.attack(self, target)
        elif verb == 'equip':
            message = self.equip(user_input[1])
        else:  # pragma: no cover
            message = 'could not take action {}'.format(' '.join(user_input))

        if self.tile.room.round_start:  # pragma: no cover
            still_enemy = False
            for tile in self.tile.room.tile_set.all():
                if tile.enemy_set.count():
                    still_enemy = True
                    break
            if still_enemy is False:
                self.tile.room.round_start = None
                self.tile.room.save()
                return message
            for tile in self.tile.room.tile_set.all():
                for enemy in tile.enemy_set.all():
                    enemy.do_combat()

        return message

    def equip(self, item):
        """
        Equip inventory item.
        """
        weapon = self.inventory.weapons.filter(name=item).first()
        if not weapon:  # pragma: no cover
            return 'You can\'t equip that!'
        self.weapon = weapon
        self.inventory.weapons.remove(weapon)
        self.save()
        return 'Equipped {}.'.format(weapon.name)

    def move(self, direction):
        """
        Change player tile.
        """
        message = ''
        move_direction = {
            'east': self.move_east,
            'north': self.move_north,
            'south': self.move_south,
            'west': self.move_west}.get(direction, None)
        if not move_direction:  # pragma: no cover
            message = 'You can\'t move {}.'.format(direction)
            return message

        room = self.tile.room

        move_direction(bool(room.round_start))

        if room != self.tile.room:
            self.health = self.max_health

        self.save()
        return 'You moved {}'.format(direction)

    def move_north(self, combat):
        """
        Change player tile north.
        """
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord - 1) &
            models.Q(x_coord=self.tile.x_coord))
        if queryset.count():
            self.tile = queryset.first()
        elif combat:
            pass  # pragma: no cover
        else:
            room = self.tile.room.go_north()
            self.tile = room.tile_set.filter(
                models.Q(y_coord=self.tile.room.grid_size - 1) &
                models.Q(x_coord=self.tile.x_coord)).first()

    def move_east(self, combat):
        """
        Change player tile east.
        """
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord) &
            models.Q(x_coord=self.tile.x_coord + 1))
        if queryset.count():
            self.tile = queryset.first()
        elif combat:
            pass  # pragma: no cover
        else:
            room = self.tile.room.go_east()
            self.tile = room.tile_set.filter(
                models.Q(y_coord=self.tile.y_coord) &
                models.Q(x_coord=0)).first()

    def move_south(self, combat):
        """
        Change player tile south.
        """
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord + 1) &
            models.Q(x_coord=self.tile.x_coord))
        if queryset.count():
            self.tile = queryset.first()
        elif combat:
            pass  # pragma: no cover
        else:
            room = self.tile.room.go_south()
            self.tile = room.tile_set.filter(
                models.Q(y_coord=0) &
                models.Q(x_coord=self.tile.x_coord)).first()

    def move_west(self, combat):
        """
        Change player tile west.
        """
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord) &
            models.Q(x_coord=self.tile.x_coord - 1))
        if queryset.count():
            self.tile = queryset.first()
        elif combat:
            pass  # pragma: no cover
        else:
            room = self.tile.room.go_west()
            self.tile = room.tile_set.filter(
                models.Q(y_coord=self.tile.y_coord) &
                models.Q(x_coord=self.tile.room.grid_size - 1)).first()


class Group(models.Model):
    """
    Instance group model.
    """

    owner = models.OneToOneField(Player, on_delete=models.CASCADE)
    black_list = models.ManyToManyField(
        Player, related_name='black_lists', blank=True)
    white_list = models.ManyToManyField(
        Player, related_name='white_lists', blank=True)


@receiver(models.signals.post_save, sender=User)
def create_new_player(sender, created=False, instance=None, **kwargs):
    """
    Create disappointment.
    """
    if created:
        Player.objects.create(user=instance, active=True,
                              name=instance.username)
        Token.objects.create(user=instance)
