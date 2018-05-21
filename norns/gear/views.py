from rest_framework import generics
from .serializers import WeaponSerializer
from .models import Weapon


class WeaponView(generics.CreateAPIView, generics.RetrieveAPIView,
                 generics.UpdateAPIView):
    """Return JSON of weapon."""
    serializer_class = WeaponSerializer

    def get_object(self):
        return Weapon.objects.get(id=self.kwargs['pk'])
