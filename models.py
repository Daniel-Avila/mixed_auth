from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class MixedAuthUser(AbstractUser):
    """Because we want to have LDAP authentication and classic
    django authentication (mainly for super users and system users)
    we need to have a mixed Authentication scheme
    """

    from_ldap = models.BooleanField(_('LDAP User'), editable=False, default=False)