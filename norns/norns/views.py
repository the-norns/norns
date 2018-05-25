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


class AboutView(TemplateView):
    """View class for the about page."""

    template_name = 'about.html'


class HomeView(TemplateView):
    """View class for the homepage."""

    template_name = 'home.html'


class StoreView(TemplateView):
    """Return store view and handle payments."""

    template_name = 'store.html'

    def post(self, request, *args, **kwargs):  # pragma: no cover
        """Handle post request for order form."""
        if 'purchase' not in kwargs:
            return render(request, 'store.html')

        purchase = kwargs['purchase'].strip().lower()

        if purchase not in PURCHASES:
            return render(request, 'store.html')

        player = get_object_or_404(Player, user=request.user, active=True)

        purchase = PURCHASES[purchase].copy()

        query = purchase.pop('query')

        stripeToken = self.request.POST['stripeToken']
        stripeTokenType = self.request.POST['stripeTokenType']
        stripeEmail = self.request.POST['stripeEmail']

        purchase.setdefault('currency', 'usd')
        purchase.setdefault('source', stripeToken)

        try:
            token = stripe.Token.retrieve(stripeToken)
            charge = stripe.Charge.create(**purchase)
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})

            print('Status is:', e.http_status)
            print('Type is:', err.get('type'))
            print('Code is:', err.get('code'))
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
            if isinstance(charge, stripe.Charge):
                charge = charge.to_dict()
                token = token.to_dict()

                if token.get('id', None) != stripeToken:
                    return render(request, 'store.html')

                if token.get('email', None) != stripeEmail:
                    return render(request, 'store.html')

                card = token.get(stripeTokenType, None)

                if card is None:
                    return render(request, 'store.html')

                if charge.get('status', None) != 'succeeded':
                    return render(request, 'store.html')

                query.first().inventory_set.add(player.inventory)
                player.inventory.save()

                return redirect('home')

        return render(request, 'store.html')
