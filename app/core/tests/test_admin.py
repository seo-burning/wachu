from django.test import Client, TestCase
from django.contrib.auth import get_user_model


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@burningb.com',
            password='test123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@burningb.com',
            password='test123',
            name='test_user'
        )
