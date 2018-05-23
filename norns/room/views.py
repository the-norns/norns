from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response

from player.models import Player

from .serializers import TileSerializer


def _serialize(response, **kwargs):
    return Response(
        {
            'message': response.get('message', None),
            'tiles': TileSerializer(
                response.get('tiles', []), many=True).data},
        **kwargs)


class RoomView(CreateAPIView, RetrieveAPIView, UpdateAPIView):
    """
    Parse form data and relevant room state.
    """

    def post(self, request, _format=None):
        """
        Response to action post.
        """
        player = get_object_or_404(Player, user=request.user)
        player = Player.get_active_player(request.user)
        user_input = self.request.data['user_input'].split()
        if not user_input:
            return {'message': 'no user input'}
        verb = user_input[0]
        if verb == 'look':
            return _serialize(player.tile.roll_tile())

        if verb == 'take':
            weapon = player.tile.weapons.filter(name=user_input[1]).first()
            if weapon:
                player.inventory.weapons.add(weapon)
                weapon.tiles.remove(player.tile)
                return _serialize({
                    'message': 'You picked up {}'.format(weapon.name),
                    'tiles': [player.tile]})
            return _serialize({
                'message': 'No {} found'.format(user_input[1])})

        return _serialize(player.handle_user_input(user_input))


class NewRoomView(CreateAPIView):
    """
    Create a new game.
    """

    def post(self, request, _format=None):
        """
        Response to create room post.
        """
        player = Player.objects.create(user=request.user, active=True)
        player.tile = player.tile.room.tile_set.order_by('?').first()
        return _serialize({
            'message': 'Welcome to Hel.',
            'tiles': player.tile.room.tile_set.all()
        }, status=201)


class TileView(RetrieveAPIView):
    """
    Get tile data.
    """

    serializer_class = TileSerializer
