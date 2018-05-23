from django.urls import path

from .views import NewRoomView, RoomView, TileView

urlpatterns = [
    path('', RoomView.as_view(), name='room'),
    path('new', NewRoomView.as_view(), name='new_room'),
    path('tile/<int:pk>', TileView.as_view(), name='tile'),
]
