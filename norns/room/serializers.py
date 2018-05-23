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
#        fields = (
#            'x_coord',
#            'y_coord',
#            'consumables_set'
#            'weapons',
#            'players',
#            'enemies',
#        )
