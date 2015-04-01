"""
web.app.tests
SDK Unit tests.
"""

# Django imports
from django.test import TestCase, Client


class ErrorTest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        delattr(self, 'client')

    def test_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
