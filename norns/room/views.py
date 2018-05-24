from django.shortcuts import get_object_or_404
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from player.models import Player

from .serializers import RoomSerializer, TileSerializer


def _serialize(player, message, **kwargs):
    return Response(
        {
            'message': message,
            'tiles': TileSerializer(
                player.tile.room.tile_set, many=True).data},
        **kwargs)


class RoomView(APIView):
    """
    Parse form data and relevant room state.
    """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, _format=None):
        """
        Response to get.
        """
        player = get_object_or_404(Player, user=request.user, active=True)
        return _serialize(player, '')

    def post(self, request, _format=None):
        """
        Response to action post.
        """
        player = get_object_or_404(Player, user=request.user, active=True)
        user_input = self.request.data['data'].split()
        if not user_input:
            return _serialize(player, 'no user input')
        verb = user_input[0]
        if verb == 'look':
            return _serialize(player, player.tile.look())

        if verb == 'take':
            weapon = player.tile.weapons.filter(name=(' ').join(user_input[1:])).first()
            consumable = player.tile.consumables.filter(name=(' ').join(user_input[1:])).first()
            if weapon:
                player.inventory.weapons.add(weapon)
                weapon.tiles.remove(player.tile)
                return _serialize(
                    player,
                    'You picked up {}'.format(weapon.name))
            if consumable:
                player.inventory.consumables.add(consumable)
                consumable.tiles.remove(player.tile)
                return _serialize(
                    player,
                    'You picked up {}'.format(consumable.name))
            return _serialize(player, 'No {} found'.format(user_input[1]))

        return _serialize(player, player.handle_user_input(user_input))


class NewRoomView(CreateAPIView):
    """
    Create a new game.
    """

    serializer_class = RoomSerializer

    def post(self, request, _format=None):
        """
        Response to create room post.
        """
        for player in Player.objects.filter(
                user=request.user, active=True).all():
            player.active = False
        player = Player.objects.create(user=request.user, active=True)
        return _serialize(player, 'Welcome to Hel.', status=201)


class TileView(RetrieveAPIView):
    """
    Get tile data.
    """

    serializer_class = TileSerializer
