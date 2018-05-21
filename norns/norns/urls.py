from django.contrib import admin
from django.urls import path, include
from .views import home_view, StoreView, about_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('store/', StoreView.as_view(), name='store'),
    path('about/', about_view, name='about'),
]
