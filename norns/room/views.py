from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.response import Response
from django.db.models import Q
from gear.models import Weapon
from player.models import Player

from .models import Room
from .serializers import RoomSerializer, TileSerializer


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
        user_input = self.request.data['user_input'].split()
        verb = user_input[0]
        if verb == 'look':
            if not player.tile.looked:
                player.tile.roll_tile()
            message = f'You see...'  # implement message output.
            return Response({
                'message': message,
                'tiles': [player.tile.id],
            })

        if verb == 'take':
            weapon = Weapon.objects.filter(
                Q(tiles=player.tile) &
                Q(name=user_input[1])).first()
            if weapon:
                player.inventory.weapons.add(weapon)
                weapon.tiles.remove(player.tile)
                return Response({
                    'message': f'You picked up {weapon.name}',
                    'tiles': [player.tile.id],
                })

        return player.handle_user_input(user_input)


class NewRoomView(CreateAPIView):
    """
    Create a new game.
    """

    def post(self, request, _format=None):
        """
        Response to create room post.
        """
        player = Player.objects.create()
        player.user = User.objects.filter(
            username=request.user.username).first()
        player.save()
        return Response({
            'message': 'Welcome to Hel.',
            'tiles': TileSerializer(player.tile.room.tile_set, many=True).data
        }, status=201)


class TileView(RetrieveAPIView):
    """
    Get tile data.
    """
    serializer_class = TileSerializer
