from django.http import HttpRequest
from directory.views import address_list, address_by_key, address_by_key_value
from django.test import TestCase
from django.test.client import Client
# import simplejson


# def test_address_list():
#     location = 'http://127.0.0.1:8000/addresses/Eric/gmail/?api=1'
#     request = HttpRequest()
#     request.method = 'PUT'
#     request.build_absolute_uri(location)
#
#     req = factory.put()
#     found = address_list(request=request)
#     assert found.status_code == 400


class TestPipeline(TestCase):
    @classmethod
    def setUp(self):
        """initialize the Django test client"""
        self.client = Client()

    def test_200(self):
        self.response = self.client.get(path='/addresses/', data={'api': '1'}, content_type="application/x-www-form-urlencoded")
        self.assertEqual(self.response.status_code, 200)

        self.response = self.client.put(path='/addresses/', data={'name': 'Eric','address': 'test', 'api': '1'}, content_type="application/x-www-form-urlencoded")
        self.assertEqual(self.response.status_code, 200)

        # self.response = self.client.get('/addresses/', data='api=1')
        # self.assertEqual(self.response.status_code, "200")

