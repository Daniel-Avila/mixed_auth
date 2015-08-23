__author__ = 'Daniel Avila'
from django.contrib.auth.backends import ModelBackend
from django_python3_ldap.auth import LDAPBackend
from django.contrib.auth import get_user_model, get_backends


class MixedBackendLDAP(LDAPBackend):
    """Our mixed auth backend"""

    def authenticate(self, *args, **kwargs):
        """Override the LDAPBackend's authenticate

        Arguments:
            username (str): String of the user name trying to authenticate

            password (str): String of the username trying to authenticate

        Returns
            object (MixedAuthUser) or None: If successful this should return an authenticated
            instance of the MixedAuthUser defined in models.py. On failure it should return None
        """

        user = super(MixedBackendLDAP, self).authenticate(*args, **kwargs)

        # TODO: Would this be useful in our context? Not sure, have to think of the implications

        # If MixedBackendLDAP is disabled this would allow any LDAP users who had
        # Authenticated once to login without LDAP.

        # if we don't want this we can delete this entire method and replace the class body with a pass
        # or use LDAPBackend directly.

        if user:
            user.set_password(kwargs['password'])
            user.save()
        return user


class MixedBackendClassic(ModelBackend):
    """A custom 'classic' django auth backend that ensures LDAP users cannot log in if
    MixedBackendLDAP is available"""

    @staticmethod
    def _is_ldap_activated():
        """Returns True if MixedBackendLDAP is activated otherwise False"""

        return MixedBackendLDAP in [b.__class__ for b in get_backends()]

    def authenticate(self, username=None, password=None, **kwargs):
        """Refuses LDAP users if MixedBackendLDAP is active"""

        if self._is_ldap_activated():
            user_model = get_user_model()
            # Determine if we are a local user
            try:
                user_model.objects.get(username=username, from_ldap=False)
            except:
                # Nope not a local user so we punt!
                return None

        # Yes we are a local user so authenticate in the normal way.
        return super(MixedBackendClassic, self).authenticate(username=username, password=password, **kwargs)