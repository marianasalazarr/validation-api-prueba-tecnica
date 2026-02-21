from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.test import TestCase

class BasicTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='test')

    def test_protected_route_401(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 401)