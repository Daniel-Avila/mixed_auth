AUTHENTICATION_BACKENDS = (
    'mixed_auth.backends.MixedAuthLDAP',
    'mixed_auth.backends.MixedAuthClassic',
)

AUTH_USER_MODEL = 'mixed_auth.models.MixedAuthUser'

# These settings should be added to your main settings file.