from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.response import Response
from django.db.models import Q
from gear.models import Weapon
from player.models import Player

from .models import Room
from .serializers import RoomSerializer


class RoomView(CreateAPIView, RetrieveAPIView, UpdateAPIView):
    """
    Parse form data and relevant room state.
    """

    serializer_class = RoomSerializer

    def get_queryset(self):
        """
        Get object for primary key.
        """
        return Room.objects.filter(id=self.kwargs['pk'])

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
            if not player.tile.looked:
                player.tile.roll_tile()
            return Response({
                'tiles': [
                    {
                        'x_coord': player.tile.x_coord,
                        'y_coord': player.tile.y_coord,
                        'contents': {
                            'weapons': [
                                w.name for w in player.tile.weapons.all()]
                        },
                    }],
            })

        if verb == 'take':
            weapon = Weapon.objects.filter(
                Q(tiles=player.tile) &
                Q(name=user_input[1])).first()
            if weapon:
                player.inventory.weapons.add(weapon)
                weapon.tiles.remove(player.tile)

        return player.handle_user_input(user_input)


class NewRoomView(CreateAPIView):
    """
    Create a new game.
    """

    def post(self, request, _format=None):
        """
        Response to create room post.
        """
        player = Player.create(user=request.user, active=True)
        room = Room.roll_room()
        player.tile = room.tiles.order_by('?').first()
        return Response({
            'message': 'Welcome to Hel.',
            'tiles': [
                {
                    'x_coord': tile.x_coord,
                    'y_coord': tile.y_coord,
                    'contents': {
                        'enemies': [(en.type.name, en.name)
                                    for en in tile.enemies.all()],
                        'players': [player.get(tile=tile).name],
                    },
                } for tile in room.tiles.all()],
        })
