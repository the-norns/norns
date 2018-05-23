from random import randint

from django.db import models
from django.dispatch import receiver


class Weapon(models.Model):
    """
    Weapon model.
    """

    name = models.CharField(max_length=255, default='Untitled')
    strength = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    ability = models.ForeignKey(
        'status.Ability', on_delete=models.SET_NULL, null=True)
    reach = models.IntegerField(default=0)

    def attack(self, player, enemy):
        """
        Attempt to damage enemy.
        """
        from room.models import Tile

        enemy = player.tile.room.tiles.enemies.filter(name=enemy)
        etiles = Tile.filter(
            models.Q(enemies=enemy) &
            models.Q(room=player.tile.room))

        if etiles.count():
            etile = etiles.first()
            if etiles.count() > 1:
                dx = abs(etile.x_axis - player.tile.x_axis)
                dy = abs(etile.y_axis - player.tile.y_axis)
                for tile in etiles.all():
                    min_axis = dx if dx < dy else dy
                    tile_dx = abs(tile.x_axis - player.tile.x_axis)
                    tile_dy = abs(tile.y_axis - player.tile.y_axis)
                    if tile_dx < min_axis or tile_dy < min_axis:
                        etile = tile
                        dx = tile_dx
                        dy = tile_dy

            if abs(player.tile.x_coord - etile.x_coord) <= self.reach \
               and abs(player.tile.y_coord - etile.y_coord) <= self.reach:
                roll = sum([randint(0, 6) for _ in range(self.strength)])
                enemy.health -= roll
            if enemy.health <= 0:
                for weapon in enemy.inventory.weapons.all():
                    weapon.tiles.add(etile)
                enemy.tiles.remove(etile)
        return {'tiles': etiles.all()}


class Consumable(models.Model):
    """
    Consumable model.
    """

    name = models.CharField(max_length=255, default='Untitled')
    ability = models.ForeignKey(
        'status.Ability', on_delete=models.SET_NULL, null=True)

    def loot(self, player):
        """
        Loot consumable.
        """
        self.tiles.remove(player.tile)
        player.consumables.add(self)

    def handle_use(self, player, target):
        """
        Use consumable.
        """
        player.consumables.remove(self)
        self.ability.use_ability(player, target)


class Inventory(models.Model):
    """
    Inventory model.
    """

    weapons = models.ManyToManyField(Weapon, blank=True)
    consumables = models.ManyToManyField(Consumable, blank=True)


@receiver(models.signals.pre_save, sender='player.Player')
def create_start_room(sender, instance=None, **kwargs):
    """
    Create initial inventory.
    """
    if not instance.inventory:
        inventory = Inventory()
        inventory.save()
        instance.inventory = inventory
