from random import randint

from django.db import models
from django.dispatch import receiver

from gear.models import Consumable, Weapon

INSTANCE_SIZE_LIMIT = 100


class Room(models.Model):
    """
    Room model.
    """

    room_north = models.OneToOneField(
        'Room',
        blank=True,
        related_name='room_south',
        on_delete=models.SET_NULL,
        null=True)
    room_east = models.OneToOneField(
        'Room',
        blank=True,
        related_name='room_west',
        on_delete=models.SET_NULL,
        null=True)
    grid_size = models.IntegerField(default=5)
    round_start = models.DateTimeField(blank=True, null=True)

    def go_north(self):
        """
        Get or generate north room.
        """
        if not self.room_north:
            self.room_north = Room.objects.create(grid_size=self.grid_size)
        return self.room_north

    def go_south(self):
        """
        Get or generate south room.
        """
        if not hasattr(self, 'room_south'):
            Room.objects.create(grid_size=self.grid_size, room_north=self)
        return self.room_south

    def go_east(self):
        """
        Get or generate east room.
        """
        if not self.room_east:
            self.room_east = Room.objects.create(grid_size=self.grid_size)
        return self.room_east

    def go_west(self):
        """
        Get or generate west room.
        """
        if not hasattr(self, 'room_west'):
            Room.objects.create(grid_size=self.grid_size, room_east=self)
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
        message = ''
        if not self.looked:
            self.looked = True
            roll = randint(0, 10)
            if roll > 3:
                message += 'You found nothing of interest.'
                return message
            if roll > 1:
                weapon = Weapon.objects.order_by('?').first()
                if weapon:
                    self.weapons.add(weapon)
                    self.save()
                    message = 'You found {}.'.format(weapon.name)
                    return message
            consumable = Consumable.objects.order_by('?').first()
            if consumable:
                self.consumables.add(consumable)
                self.save()
                message = 'You found {}.'.format(consumable.name)
                return message


@receiver(models.signals.pre_save, sender='player.Player')
def create_start_room(sender, instance=None, **kwargs):
    """
    Create initial room.
    """
    if not hasattr(instance, 'tile'):
        cls = type(instance)
        room = None
        for origin in cls.objects.order_by('?').values('origin_id').distinct():
            origin_id = origin['origin_id']
            if (
                    cls.objects.filter(origin_id=origin_id).count()
                    < INSTANCE_SIZE_LIMIT):
                room = Room.objects.get(pk=origin_id)
                break
        if room is not None:
            pass
        elif Room.objects.filter(room_north=None, room_east=None).count():
            room = Room.objects.filter(
                room_north=None, room_east=None).order_by('?').first()
        else:
            room = Room.objects.create()
        instance.origin = room
        instance.tile = room.tile_set.order_by('?').first()


@receiver(models.signals.post_save, sender=Room)
def populate_tiles(sender, created=False, instance=None, **kwargs):
    """
    Create disappointment.
    """
    if created:
        for x in range(instance.grid_size):
            for y in range(instance.grid_size):
                Tile.objects.create(x_coord=x, y_coord=y, room=instance)
