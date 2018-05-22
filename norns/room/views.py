from random import randint

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics

from enemy.models import Enemy
from gear.models import Weapon
from player.models import Player

from .models import Room, Tile
from .serializers import RoomSerializer


class RoomView(generics.CreateAPIView, generics.RetrieveAPIView,
               generics.UpdateAPIView):
    """Parse form data and relevant room state."""

    serializer_class = RoomSerializer
    grid_size = 5

    @staticmethod
    def roll_tile(tile):
        """
        Create disapointment.
        """
        roll = randint(0, 10)
        if roll < 2:
            Weapon.order_by('?').first().tiles.add(tile)

    def roll_room(self, direction, prev_room):
        """
        Generate room.
        """
        room = Room.create()
        if direction == 'north':
            room.room_south = prev_room
        if direction == 'east':
            room.room_west = prev_room
        if direction == 'south':
            room.room_north = prev_room
        if direction == 'west':
            room.room_east = prev_room
        room.save()

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                tile = Tile.create(x_coord=x, y_coord=y, room=room)
                roll = randint(0, 10)
                if roll == 1:
                    Enemy.order_by('?').first().tiles.add(tile)

        return room

    def move_player(self, player, direction):
        """
        Change player tile.
        """
        if direction == 'north':
            queryset = Tile.objects.filter(
                Q(y_coord=player.tile.y_coord - 1) &
                Q(x_coord=player.tile.x_coord))
            if queryset.count():
                player.tile = queryset.first()
            else:
                player.tile = Tile.objects.filter(
                    Q(y_coord=self.grid_size - 1) &
                    Q(x_coord=player.tile.x_coord))
        elif direction == 'east':
            queryset = Tile.objects.filter(
                Q(y_coord=player.tile.y_coord) &
                Q(x_coord=player.tile.x_coord + 1))
            if queryset.count():
                player.tile = queryset.first()
            else:
                player.tile = Tile.objects.filter(
                    Q(y_coord=player.tile.y_coord) &
                    Q(x_coord=0))
        elif direction == 'south':
            queryset = Tile.objects.filter(
                Q(y_coord=player.tile.y_coord + 1) &
                Q(x_coord=player.tile.x_coord))
            if queryset.count():
                player.tile = queryset.first()
            else:
                player.tile = Tile.objects.filter(
                    Q(y_coord=0) &
                    Q(x_coord=player.tile.x_coord))
        elif direction == 'west':
            queryset = Tile.objects.filter(
                Q(y_coord=player.tile.y_coord) &
                Q(x_coord=player.tile.x_coord - 1))
            if queryset.count():
                player.tile = queryset.first()
            else:
                player.tile = Tile.objects.filter(
                    Q(y_coord=player.tile.y_coord) &
                    Q(x_coord=self.grid_size - 1))

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
        if 'pk' in self.kwargs:
            if user_input[0] == 'look':
                if not player.tile.looked:
                    self.roll_tile(player.tile)
                return super().retrieve(request, self.kwargs['pk'])

            if user_input[0] == 'go':
                self.move_player(player, user_input[1])

        else:
            return self.roll_room(user_input[1], self.kwargs['prev_room_id'])
