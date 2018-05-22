from django.urls import path

from .views import RoomView, NewRoomView

urlpatterns = [
    path('', RoomView.as_view(), name='room'),
    path('new', NewRoomView.as_view(), name='new_room')
]
