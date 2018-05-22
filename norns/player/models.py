from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    """
    Instance group model.
    """

    owner = models.OneToOneField('Player', on_delete=models.CASCADE)
    black_list = models.ManyToManyField(
        'Player', related_name='black_lists', blank=True)
    white_list = models.ManyToManyField(
        'Player', related_name='white_lists', blank=True)


class Player(models.Model):
    """
    Player model.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, default='Unnamed')
    health = models.IntegerField(default=10)

    abilities = models.ManyToManyField('status.Ability', blank=True)
    inventory = models.OneToOneField(
        'gear.Inventory',
        blank=True,
        on_delete=models.CASCADE,
        null=True)
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
            self.move(user_input[1])
        if verb == 'attack':
            self.weapon.attack(user_input[1])
        if verb == 'equip':
            self.equip(user_input[1])

    def equip(self, item):
        """
        Equip inventory item.
        """
        weapon = self.inventory.weapons.get(name=item)
        self.weapon = weapon
        self.inventory.weapons.remove(weapon)

    def move(self, direction):
        """
        Change player tile.
        """
        if direction == 'north':
            queryset = self.tile.room.tile_set.filter(
                models.Q(y_coord=self.tile.y_coord - 1) &
                models.Q(x_coord=self.tile.x_coord))
            if queryset.count():
                self.tile = queryset.first()
            else:
                room = self.tile.room.go_north()
                self.tile = room.tile_set.filter(
                    models.Q(y_coord=self.tile.room.grid_size - 1) &
                    models.Q(x_coord=self.tile.x_coord))
        elif direction == 'east':
            queryset = self.tile.room.tile_set.filter(
                models.Q(y_coord=self.tile.y_coord) &
                models.Q(x_coord=self.tile.x_coord + 1))
            if queryset.count():
                self.tile = queryset.first()
            else:
                room = self.tile.room.go_east()
                self.tile = room.tile_set.filter(
                    models.Q(y_coord=self.tile.y_coord) &
                    models.Q(x_coord=0))
        elif direction == 'south':
            queryset = self.tile.room.tile_set.filter(
                models.Q(y_coord=self.tile.y_coord + 1) &
                models.Q(x_coord=self.tile.x_coord))
            if queryset.count():
                self.tile = queryset.first()
            else:
                room = self.tile.room.go_south()
                self.tile = room.tile_set.filter(
                    models.Q(y_coord=0) &
                    models.Q(x_coord=self.tile.x_coord))
        elif direction == 'west':
            queryset = self.tile.room.tile_set.filter(
                models.Q(y_coord=self.tile.y_coord) &
                models.Q(x_coord=self.tile.x_coord - 1))
            if queryset.count():
                self.tile = queryset.first()
            else:
                room = self.tile.room.go_west()
                self.tile = room.tile_set.filter(
                    models.Q(y_coord=self.tile.y_coord) &
                    models.Q(x_coord=self.tile.room.grid_size - 1))
