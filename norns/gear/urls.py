from django.urls import path
from .views import WeaponView

urlpatterns = [
    path('weapon/<int:pk>', WeaponView.as_view(), name='weapon'),
]
