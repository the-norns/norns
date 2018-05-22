from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from gear.models import Weapon, Inventory
from room.models import Tile
from status.models import Ability


class Player(models.Model):
    """
    Player model.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, default='Unnamed')
    health = models.IntegerField(default=10)
    abilities = models.ManyToManyField(Ability, blank=True)
    weapon = models.ForeignKey(
        Weapon, blank=True, on_delete=models.CASCADE, null=True)
    tile = models.ForeignKey(
        Tile, blank=True, on_delete=models.CASCADE, null=True)
    inventory = models.OneToOneField(
        Inventory,
        blank=True,
        null=True,
        related_name='player',
        on_delete=models.CASCADE)

    def handle_user_input(self, user_input):
        verb = user_input[0]
        if verb == 'go':
            self.move(user_input[1])
        if verb == 'attack':
            self.weapon.attack(self, user_input[1])
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
            queryset = Tile.objects.filter(
                Q(y_coord=self.tile.y_coord - 1) &
                Q(x_coord=self.tile.x_coord) &
                Q(room=self.tile.room))
            if queryset.count():
                self.tile = queryset.first()
            else:
                room = self.tile.room.room_north
                if not room:
                    room = self.tile.room.roll_room(direction)
                self.tile = Tile.objects.filter(
                    Q(y_coord=self.tile.room.grid_size - 1) &
                    Q(x_coord=self.tile.x_coord) &
                    Q(room=room))
        elif direction == 'east':
            queryset = Tile.objects.filter(
                Q(y_coord=self.tile.y_coord) &
                Q(x_coord=self.tile.x_coord + 1) &
                Q(room=self.tile.room))
            if queryset.count():
                self.tile = queryset.first()
            else:
                room = self.tile.room.room_east
                if not room:
                    room = self.tile.room.roll_room(direction)
                self.tile = Tile.objects.filter(
                    Q(y_coord=self.tile.y_coord) &
                    Q(x_coord=0) &
                    Q(room=room))
        elif direction == 'south':
            queryset = Tile.objects.filter(
                Q(y_coord=self.tile.y_coord + 1) &
                Q(x_coord=self.tile.x_coord) &
                Q(room=self.tile.room))
            if queryset.count():
                self.tile = queryset.first()
            else:
                room = self.tile.room.room_south
                if not room:
                    room = self.tile.room.roll_room(direction)
                self.tile = Tile.objects.filter(
                    Q(y_coord=0) &
                    Q(x_coord=self.tile.x_coord) &
                    Q(room=room))
        elif direction == 'west':
            queryset = Tile.objects.filter(
                Q(y_coord=self.tile.y_coord) &
                Q(x_coord=self.tile.x_coord - 1) &
                Q(room=self.tile.room))
            if queryset.count():
                self.tile = queryset.first()
            else:
                room = self.tile.room.room_west
                if not room:
                    room = self.tile.room.roll_room(direction)
                self.tile = Tile.objects.filter(
                    Q(y_coord=self.tile.y_coord) &
                    Q(x_coord=self.tile.room.grid_size - 1) &
                    Q(room=room))
