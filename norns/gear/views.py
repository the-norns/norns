from rest_framework import generics

from .models import Weapon
from .serializers import WeaponSerializer


class WeaponView(generics.CreateAPIView, generics.RetrieveAPIView,
                 generics.UpdateAPIView):
    """Return JSON of weapon."""
    serializer_class = WeaponSerializer

    def get_object(self):
        return Weapon.objects.get(id=self.kwargs['pk'])
