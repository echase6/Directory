from django.test import TestCase
from django.test.client import Client


class TestPipeline(TestCase):
    @classmethod
    def setUp(self):
        """initialize the Django test client"""
        self.client = Client()

    def test_200(self):
        self.response = self.client.get(path='/addresses/', data={'api': '1'},
                                        content_type="application/x-www-form-urlencoded")
        self.assertEqual(self.response.status_code, 200)
