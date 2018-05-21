"""
Norns URL Configuration.
"""

from django.contrib import admin
from django.urls import path

from .views import about_view, home_view, store_view

__all__ = ('urlpatterns', )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('store/', store_view, name='store'),
    path('about/', about_view, name='about'),
]
