from django.urls import path
from .views import RoomView

urlpatterns = [
    path('<int:pk>', RoomView.as_view(), name='room'),
]
