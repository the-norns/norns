from rest_framework import serializers

from .models import Room, Tile


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class TileSerializer(serializers.ModelSerializer):
    # players = tile.players

    class Meta:
        model = Tile
        fields = (
            'x_coord',
            'y_coord',
            'consumables',
            'weapons',
            'player_set',
            'enemy_set',
        )
        depth = 1
