from rest_framework import generics
from .serializers import RoomSerializer


class RoomView(generics.CreateAPIView, generics.RetrieveAPIView,
               generics.UpdateAPIView):
    serializer_class = RoomSerializer
