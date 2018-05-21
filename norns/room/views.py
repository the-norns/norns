from rest_framework import generics
from .serializers import RoomSerializer
from gear.models import Weapon
from .models import Room, Tile
from random import randint


class RoomView(generics.CreateAPIView, generics.RetrieveAPIView,
               generics.UpdateAPIView):
    """Parse form data and relevant room state."""
    serializer_class = RoomSerializer

    def roll(self, tile):
        roll = randint(0, 10)
        if roll < 2:
            Weapon.order_by('?').first().tiles.add(tile)

    def get_queryset(self):
        return Room.objects.filter(id=self.kwargs['pk'])

    def post(self, request, format=None):
        if 'pk' in self.kwargs:
            tile = Tile.objects.get(id=self.kwargs['tile_id'])
            if self.request.data['verb'] == 'look':
                if not tile.looked:
                    self.roll(tile)
                return super().retrieve(request, self.kwargs['pk'])

#          else:
#              room = Room.create()
#              grid_size = 5
#              for x in range(grid_size):
#                  for y in range(grid_size):
#                      Tile.create(x_coord=x, y_coord=y
