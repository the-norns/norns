from rest_framework import serializers

from .models import Enemy


class EnemySerializer(serializers.ModelSerializer):
    """Serializer for enemy model."""

    class Meta:
        """Meta class for model fields."""

        model = Enemy
        fields = ('name', 'health')
