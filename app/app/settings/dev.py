from .common import *

ALLOWED_HOSTS += ['localhost']

DEBUG = True
INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]
# WSGI application
WSGI_APPLICATION = 'app.wsgi.dev.application'


INTERNAL_IPS = ('172.18.0.1',)
