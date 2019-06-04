from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from store.models import Store
from store.serializers import StoreSerializer

STORE_URL = reverse('store:store-list')


def sample_store(**params):
    """Create and return a sample store"""
    defaults = {
        'insta_id': 'test_id',
        'is_updated': True,
        'name': 'Teststore',
        'follower': 3214,
        'following': 24145,
        'post_num': 241512,
        'description': "afassss" + "\n" + "ipsum",
        'phone': "195120i8",
        'email': "su.seo@burningb.com",
        'insta_url': 'http://www.instagram.com/' + "Teststore" + '/',
        'profile_image': "https://bit.ly/2WMDD6u"
    }
    defaults.update(params)

    return Store.objects.create(**defaults)


class PublicStoreAPITests(TestCase):
    """Test unauthenticated store API access"""

    def setUp(self):
        self.client = APIClient()

    def test_require_auth(self):
        """Test the authentication is required"""
        res = self.client.get(STORE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStoreAPITests(TestCase):
    """Test the authorized store API access"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@burningb.com',
            'pawnalksfkwl223'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_store(self):
        """Test retrieving store"""
        sample_store()
        sample_store(insta_id='test2')

        res = self.client.get(STORE_URL)

        stores = Store.objects.all().order_by('-insta_id')
        serializer = StoreSerializer(stores, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
