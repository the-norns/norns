"""
Core views.
"""

from django.shortcuts import render


def home_view(request):
    """Return home view."""
    return render(request, 'home.html')


def store_view(request):
    """Return store view."""
    return render(request, 'store.html')


def about_view(request):
    """Return about view."""
    return render(request, 'about.html')
