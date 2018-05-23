from rest_framework import serializers

from .models import Room, Tile


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room


class TileSerializer(serializers.ModelSerializer):
    # players = tile.players

    class Meta:
        model = Tile
        fields = '__all__'
        depth = 1
