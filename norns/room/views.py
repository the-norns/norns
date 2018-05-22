from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView)
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
        user_input = self.request.data['user_input'].split()
        verb = user_input[0]
        if verb == 'look':
            if not player.tile.looked:
                player.tile.roll_tile()
            return super().retrieve(request, self.kwargs['pk'])
        if verb == 'take':
            weapon = Weapon.objects.filter(
                Q(tiles=player.tile) &
                Q(name=user_input[1])).first()
            if weapon:
                player.inventory.weapons.add(weapon)
                weapon.tiles.remove(player.tile)

        player.handle_user_input(user_input)
