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

    # players = tile.players

    DEMO = {
        'tiles': [
            {
                'x_coord': 'player.tile.x_coord',
                'y_coord': 'player.tile.y_coord',
                'contents': {
                    'weapons': [
                        'w.name for w in player.tile.weapons.all()']
                },
            }],
    }

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
        depth = 1
