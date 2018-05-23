from random import randint

from django.db import models
from django.dispatch import receiver

from gear.models import Consumable, Weapon


class Room(models.Model):
    """
    Room model.
    """

    room_north = models.OneToOneField(
        'Room',
        blank=True,
        related_name='room_south',
        on_delete=models.SET_NULL,
        null=True,
    )
    room_east = models.OneToOneField(
        'Room',
        blank=True,
        related_name='room_west',
        on_delete=models.SET_NULL,
        null=True,
    )
    grid_size = models.IntegerField(default=5)

    def go_north(self):
        """
        Get or generate north room.
        """
        if not self.room_north:
            room = Room(grid_size=self.grid_size)
            self.room_north = room
            room.save()
        return self.room_north

    def go_south(self):
        """
        Get or generate south room.
        """
        if not hasattr(self, 'room_south'):
            Room(grid_size=self.grid_size, room_north=self).save()
        return self.room_south

    def go_east(self):
        """
        Get or generate east room.
        """
        if not self.room_east:
            room = Room(grid_size=self.grid_size)
            self.room_east = room
            room.save()
        return self.room_east

    def go_west(self):
        """
        Get or generate west room.
        """
        if not hasattr(self, 'room_west'):
            Room(grid_size=self.grid_size, room_east=self).save()
        return self.room_west


class Tile(models.Model):
    """
    Tile model.
    """

    looked = models.BooleanField(default=False)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    desc = models.TextField(blank=True)

    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    consumables = models.ManyToManyField(Consumable, blank=True)
    weapons = models.ManyToManyField(Weapon, blank=True)

    def look(self):
        """
        Create disappointment.
        """
        if not self.looked:
            self.looked = True
            roll = randint(0, 10)
            if roll > 2:
                return
            if roll > 1:
                weapon = Weapon.objects.order_by('?').first()
                weapon.save()
                self.weapons.add(weapon)
            consumable = Consumable.objects.order_by('?').first()
            consumable.save()
            self.consumables.add(consumable)


@receiver(models.signals.pre_save, sender='player.Player')
def create_start_room(sender, instance=None, **kwargs):
    """
    Create initial room.
    """
    if not instance.tile:
        room = Room()
        room.save()
        instance.origin = room
        instance.tile = room.tile_set.first()


@receiver(models.signals.post_save, sender=Room)
def populate_tiles(sender, instance=None, **kwargs):
    """
    Create disappointment.
    """
    for x in range(instance.grid_size):
        for y in range(instance.grid_size):
            Tile(x_coord=x, y_coord=y, room=instance).save()
