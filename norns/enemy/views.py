from rest_framework import generics

from .models import Enemy
from .serializers import EnemySerializer


class WeaponView(generics.CreateAPIView, generics.RetrieveAPIView,
                 generics.UpdateAPIView):
    """Return JSON of enemy."""

    serializer_class = EnemySerializer

    def get_object(self):
        """Get an enemy object."""
        return Enemy.objects.get(id=self.kwargs['pk'])
