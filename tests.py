from django.test import TestCase
from django.test import mock
from django.contrib.auth import get_user_model
from .backends import MixedBackendLDAP

class TestLDAPAuth(TestCase):


    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",
                                                         email="test@localhost",
                                                         password="password")
        self.user.save()

    @mock.patch('django_python3_ldap.ldap.authenticate')
    def test_auth_ldap(self, mock_auth):
        """Can we actually authenticate via LDAP?"""
        # Setup our mock
        # this test doesnt do much other than make sure we have all the pieces in place.
        mock_auth.return_value = self.user
        auth_back = MixedBackendLDAP()
        user = auth_back.authenticate(**{'username': 'testuser', 'password':'password'})
        self.assertEqual(user, self.user)