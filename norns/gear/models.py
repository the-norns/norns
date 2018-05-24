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
        'status.Ability', on_delete=models.CASCADE, null=True)
    reach = models.IntegerField(default=0)

    def attack(self, source, target):
        """
        Attempt to damage target.
        """
        if not target.name:
            return 'You can\'t attack {}.'.format(target.name)

        message = ''
        if abs(source.tile.x_coord - target.tile.x_coord) <= self.reach \
           and abs(source.tile.y_coord - target.tile.y_coord) <= self.reach:
            roll = sum([randint(0, 6) for _ in range(self.strength)])
            target.health -= roll
            if roll == self.strength * 6:
                message += 'Crit!\n'
            message += '{} hit {} for {} damage.\n'.format(
                source.name, target.name, roll)

        if target.health <= 0:
            message += ' {} was slain!\n'.format(target.name)
            for weapon in target.inventory.weapons.all():
                weapon.tiles.add(target.tile)
                target.inventory.remove(weapon)
            for consumable in target.inventory.consumables.all():
                consumable.tiles.add(target.tile)
                target.inventory.remove(consumable)
            if hasattr(target, 'user'):
                message += ' You have died.\n'
                #  target.tile = 'target.origin.tile_set.order_by('?').first()
            else:
                target.delete()

        return message


class Consumable(models.Model):
    """
    Consumable model.
    """

    name = models.CharField(max_length=255, default='Untitled')
    ability = models.ForeignKey('status.Ability', on_delete=models.CASCADE)

    def loot(self, player):
        """
        Loot consumable.
        """
        self.tile_set.remove(player.tile)
        player.inventory.consumables.add(self)
        return 'You looted {}!'.format(self.name)

    def handle_use(self, player, target):
        """
        Use consumable.
        """
        if not player.inventory.consumables.filter(id=self.id).count():
            return 'You don\'t have {}'.format(self.name)
        player.inventory.consumables.remove(self)
        return self.ability.use_ability(player, target)


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
        instance.inventory = Inventory.objects.create()


@receiver(models.signals.pre_save, sender='enemy.Enemy')
def create_enemy_inventory(sender, instance=None, **kwargs):
    """
    Create enemy inventory.
    """
    if not instance.inventory:
        instance.inventory = Inventory.objects.create()
