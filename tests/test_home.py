from django.test import TestCase
from django.test.client import Client


class Home(TestCase):
    """
    Tests home view.
    """
    def test_get(self):
        response = Client().get('/')
        # TODO: Activate this test
        # self.assertEqual(response.status_code, 200)
