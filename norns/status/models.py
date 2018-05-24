from django.dispatch import receiver
from django.db import models
from django.dispatch import receiver


class Action:
    """
    Generic ability action class.
    """

    actions = {}

    @classmethod
    def run(cls, ability, player, target, distance):
        """
        Use potion on player.
        """
        setattr(target, cls.stat, getattr(target, cls.stat) + cls.quantity)

    @classmethod
    def get_model_field(cls):
        """
        Generate field from registered subclasses.
        """
        choices = (
            (short_name, subc.__name__)
            for short_name, subc in cls.actions.items())
        max_length = max(map(len, cls.actions.keys()))
        return models.CharField(
            max_length=max_length,
            choices=choices)


class MinorHeal(Action):
    """
    Heal target for 5.
    """

    short_name = 'MH'
    stat = 'health'
    quantity = 5


for action in (MinorHeal,):
    action.actions[action.short_name] = action


class Ability(models.Model):
    """
    Generic ability.
    """

    name = models.CharField(max_length=255)
    range = models.IntegerField(default=0)
    action = Action.get_model_field()

    def use_ability(self, player, target):
        """
        Validate and dispatch action.
        """
        player_tile = player.tile
        target_tile = target.tile
        if player_tile.room != target_tile.room:
            return 'No target found.'
        distance = (
            abs(player_tile.x_coord - target_tile.x_coord) +
            abs(player_tile.y_coord - target_tile.y_coord))
        if not 0 <= distance <= self.range:
            return 'Out of range.'

        Action.actions[self.action].run(self, player, target, distance)
        return 'You used {}'.format(self.name)


@receiver(models.signals.pre_save, sender='gear.Consumable')
def create_consumable_ability(sender, instance=None, **kwargs):
    """
    Create an ability for a consumable.
    """
    if not instance.ability:
        if Ability.objects.count():
            instance.ability = Ability.objects.order_by('?').first()
        else:
            instance.ability = Ability.objects.create()
