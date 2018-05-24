from rest_framework import serializers

from .models import Room, Tile


class RoomSerializer(serializers.ModelSerializer):
    """
    Room serializer.
    """

    class Meta:
        """
        Room serializer meta.
        """

        model = Room
        fields = '__all__'


class TileSerializer(serializers.ModelSerializer):
    """
    Tile serializer.
    """

    class Meta:
        """
        Tile serializer meta.
        """

        model = Tile
        fields = (
            'x_coord',
            'y_coord',
            'consumables',
            'weapons',
            'player_set',
            'enemy_set',
        )
        depth = 3
