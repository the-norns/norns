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
    health = models.IntegerField(default=10)

    abilities = models.ManyToManyField('status.Ability', blank=True)
    inventory = models.OneToOneField(
        'gear.Inventory',
        on_delete=models.CASCADE)
    origin = models.ForeignKey('room.Room', on_delete=models.CASCADE)
    tile = models.ForeignKey(
        'room.Tile', blank=True, on_delete=models.SET_NULL, null=True)
    weapon = models.ForeignKey(
        'gear.Weapon',
        blank=True,
        related_name='equiped_set',
        on_delete=models.SET_NULL,
        null=True)

    def handle_user_input(self, user_input):
        """
        Handle input.
        """
        verb = user_input[0]
        if verb == 'go':
            return self.move(user_input[1])
        if verb == 'attack':
            return self.weapon.attack(self, user_input[1])
        if verb == 'equip':
            return self.equip(user_input[1])
        return 'could not take action {}'.format(' '.join(user_input))

    def equip(self, item):
        """
        Equip inventory item.
        """
        weapon = self.inventory.weapons.filter(name=item).first()
        self.weapon = weapon
        self.inventory.weapons.remove(weapon)
        return 'Equipped {}'.format(self.name)

    def move(self, direction):
        """
        Change player tile.
        """
        move_direction = {
            'east': self.move_east,
            'north': self.move_north,
            'south': self.move_south,
            'west': self.move_west}.get(direction, None)
        if not move_direction:
            return 'You can\'t move {}.'.format(direction)

        return move_direction() or ''

    def move_north(self):
        """
        Change player tile north.
        """
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord - 1) &
            models.Q(x_coord=self.tile.x_coord))
        if queryset.count():
            self.tile = queryset.first()
        else:
            room = self.tile.room.go_north()
            self.tile = room.tile_set.filter(
                models.Q(y_coord=self.tile.room.grid_size - 1) &
                models.Q(x_coord=self.tile.x_coord)).first()

    def move_east(self):
        """
        Change player tile east.
        """
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord) &
            models.Q(x_coord=self.tile.x_coord + 1))
        if queryset.count():
            self.tile = queryset.first()
        else:
            room = self.tile.room.go_east()
            self.tile = room.tile_set.filter(
                models.Q(y_coord=self.tile.y_coord) &
                models.Q(x_coord=0)).first()

    def move_south(self):
        """
        Change player tile south.
        """
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord + 1) &
            models.Q(x_coord=self.tile.x_coord))
        if queryset.count():
            self.tile = queryset.first()
        else:
            room = self.tile.room.go_south()
            self.tile = room.tile_set.filter(
                models.Q(y_coord=0) &
                models.Q(x_coord=self.tile.x_coord)).first()

    def move_west(self):
        """
        Change player tile west.
        """
        queryset = self.tile.room.tile_set.filter(
            models.Q(y_coord=self.tile.y_coord) &
            models.Q(x_coord=self.tile.x_coord - 1))
        if queryset.count():
            self.tile = queryset.first()
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
        Player(user=instance, active=True).save()
        Token(user=instance).save()
