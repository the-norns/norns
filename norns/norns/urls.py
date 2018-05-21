from django.contrib import admin
from django.urls import path, include
from .views import HomeView, StoreView, about_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('store/', StoreView.as_view(), name='store'),
    path('about/', about_view, name='about'),
]
