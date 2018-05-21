from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import stripe


def home_view(request):
    """Return home view."""
    return render(request, 'home.html')


class StoreView(TemplateView):
    """Return store view and handle payments."""

    template_name = 'store.html'

    def get_context_data(self, **kwargs):
        """Get request for homepage class view."""
        context = super().get_context_data(**kwargs)
        return context

    def post(self, *args, **kwargs):
        """Handle post request for order form."""
        stripe.api_key = "sk_test_bDdZgeBXWJOYecXwD7W2ta0n"

        token = self.request.POST['stripeToken']

        charge = stripe.Charge.create(
            amount=2000,
            currency='usd',
            description='Example charge',
            source=token,
        )
        return render(self.request, 'store.html', {'message': 'Thanks for your money, sucker!'})


def about_view(request):
    """Return about view."""
    return render(request, 'about.html')
