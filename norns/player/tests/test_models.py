from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy

from ..models import Player
# from factory.django import DjangoModelFactory
# from django.urls import reverse_lazy


class TestModels(TestCase):
    """
    Test Player model.
    """

    def setUp(self):
        """
        Create player models.
        """
        self.user = mommy.make(User)

    def tearDown(self):
        """
        Destroy player models.
        """
        Player.objects.all().delete()

    def test_player_exists(self):
        """
        Validate player created.
        """
        self.assertGreaterEqual(
            Player.objects.filter(user=self.user).count(), 1)
