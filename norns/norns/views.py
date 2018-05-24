"""
Core views.
"""

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from gear.models import Consumable, Weapon
from player.models import Player

stripe.api_key = settings.STRIPE_SECRET_KEY

PURCHASES = {
    'thor': {
        'amount': 2000,
        'description': 'Norns player Thor',
        'query': Weapon.objects.filter(name='Mjolnir hammer of Thor'),
    },
    'walker': {
        'amount': 200,
        'description': 'Norns weapon Walker',
        'query': Weapon.objects.filter(name='Orichalcum Walker of Speed'),
    },
    'safe': {
        'amount': 99,
        'description': 'Norns room safe',
        'query': Consumable.objects.filter(name='Safe Room'),
    }
}



class HomeView(TemplateView):
    """View class for the homepage."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """Get request for homepage class view."""
        context = super().get_context_data(**kwargs)
        return context


class StoreView(TemplateView):
    """Return store view and handle payments."""

    template_name = 'store.html'

    def post(self, request, *args, **kwargs):
        """Handle post request for order form."""
        if 'purchase' not in kwargs:
            return {}

        purchase = kwargs['purchase'].strip().lower()

        if purchase not in PURCHASES:
            return {}

        player = get_object_or_404(Player, user=request.user, active=True)

        purchase = PURCHASES[purchase]

        query = purchase.pop('query')

        csrfmiddlewaretoken = self.request.POST['csrfmiddlewaretoken']
        stripeToken = self.request.POST['stripeToken']
        stripeTokenType = self.request.POST['stripeTokenType']
        stripeEmail = self.request.POST['stripeEmail']

        try:
            token = stripe.Token.retrieve(stripeToken)

            purchase.setdefault(currency='usd', source=stripeToken)

            charge = stripe.Charge.create(**purchase)
            # Use Stripe's library to make requests...
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})

            print('Status is:', e.http_status)
            print('Type is:', err.get('type'))
            print('Code is:', err.get('code'))
            # param is '' in this case
            print('Param is:', err.get('param'))
            print('Message is:', err.get('message'))
        except stripe.error.RateLimitError as e:
            print('Too many requests made to the API too quickly', e)
        except stripe.error.InvalidRequestError as e:
            print('Invalid parameters were supplied to Stripe\'s API', e)
        except stripe.error.AuthenticationError as e:
            print('Authentication with Stripe\'s API failed')
            print('(maybe you changed API keys recently)', e)
        except stripe.error.APIConnectionError as e:
            print('Network communication with Stripe failed', e)
        except stripe.error.StripeError as e:
            print('Display a very generic error to the user, and maybe send')
            print('yourself an email', e)
        except Exception as e:
            print('Something else happened, completely unrelated to Stripe', e)
        else:
            print(charge)

            if isinstance(charge, stripe.Charge):
                import pdb; pdb.set_trace()

                print(query.first())

                return redirect('home')

        return {}


def about_view(request):
    """Return about view."""
    return render(request, 'about.html')
