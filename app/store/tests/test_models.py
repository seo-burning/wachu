from django.test import TestCase
from django.contrib.auth import get_user_model

from store import models


def sample_user(email='test@burningb.com', password='aaknl2lnlsf'):
    """Create user for test"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_categeory_str(self):
        """Test the categeory string representation"""
        categeory = models.Category.objects.create(
            name='Fashion'
        )

        self.assertEqual(str(categeory), categeory.name)
