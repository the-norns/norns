"""
Norns URL Configuration.
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

from .views import HomeView, StoreView, about_view

__all__ = ('urlpatterns', )


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', about_view, name='about'),
    path('accounts/', include('registration.backends.hmac.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/gear/', include('gear.urls')),
    path('api/v1/', include('room.urls')),
    path('store/', StoreView.as_view(), name='store'),
    path('store/<str:purchase>', StoreView.as_view(), name='store_purchase'),
    path('login', views.obtain_auth_token),
]
