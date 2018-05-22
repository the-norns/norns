"""
Core views.
"""

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """View class for the homepage."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """Get request for homepage class view."""
        context = super().get_context_data(**kwargs)
        # import pdb; pdb.set_trace()
        return context


class StoreView(TemplateView):
    """Return store view and handle payments."""

    template_name = 'store.html'

    def get_context_data(self, **kwargs):
        """Get request for store class view."""
        context = super().get_context_data(**kwargs)
        return context

    def post(self, *args, **kwargs):
        """Handle post request for order form."""
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # import pdb; pdb.set_trace()

        token = self.request.POST['stripeToken']

        charge = stripe.Charge.create(
            amount=2000,
            currency='usd',
            description='Example charge',
            source=token,
        )
        return redirect('home')


def about_view(request):
    """Return about view."""
    return render(request, 'about.html')
