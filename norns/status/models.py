from django.dispatch import receiver
from django.db import models
from django.http import HttpResponseBadRequest


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

    name = models.CharField(max_length=255, blank=True, null=True)
    range = models.IntegerField(default=0)
    action = Action.get_model_field()

    def use_ability(self, player, target):
        """
        Validate and dispatch action.
        """
        player_tile = player.tile
        target_tile = player_tile.room.tile_set.filter(
            models.Q(enemy=target) | models.Q(player=player)).first()
        if not target_tile:
            return HttpResponseBadRequest()
        distance = (
            abs(player_tile.x_coord - target_tile.x_coord) +
            abs(player_tile.y_coord - target_tile.y_coord))
        if not 0 <= distance <= self.range:
            return HttpResponseBadRequest()

        Action.actions[self.action].run(self, player, target, distance)
        return {}


# @receiver(models.signals.pre_save, sender='gear.Consumable')
# def create_consumable_ability(sender, instance=None, **kwargs):
#     """
#     Create an ability for a consumable.
#     """
# 
#     #if not hasattr(instance, 'ability'):
#         #pass
#         #ability = Ability.objects.order_by('?').first()
#         #instance.ability = ability
