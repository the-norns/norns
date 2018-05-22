from django.db import models


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

#    def attack(self, enemy):
#        """
#        Attempt to damage enemy.
#        """


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
