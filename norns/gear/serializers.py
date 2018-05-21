from rest_framework import serializers
from .models import Weapon


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ('name', 'strength', 'agility')
