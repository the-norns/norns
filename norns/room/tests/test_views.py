from django.test import TestCase

from ..views import NewRoomView, RoomView


class TestViews(TestCase):
    """
    Test views.
    """

    def test_valid_view(self):
        """
        Use import.
        """
        self.assertIsNotNone(NewRoomView.as_view())
        self.assertIsNotNone(RoomView.as_view())
