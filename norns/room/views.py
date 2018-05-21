from rest_framework import generics
from rest_framework.response import Response
from .serializers import RoomSerializer
from gear.serializers import WeaponSerializer
from gear.models import Weapon
from .models import Room


class RoomView(generics.CreateAPIView, generics.RetrieveAPIView,
               generics.UpdateAPIView):
    """Parse form data and relevant room state."""
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(id=self.kwargs['pk'])

    def post(self, request, pk=None):
        if self.request.data['verb'] == 'look':
            return Response({
                'weapons': WeaponSerializer(
                    Weapon.objects.filter(
                        tiles__id=self.request.data['tile_id']),
                    many=True,
                    ).data})
