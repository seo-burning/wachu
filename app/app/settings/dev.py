from .common import *

ALLOWED_HOSTS += ['localhost']

DEBUG = True

# WSGI application
WSGI_APPLICATION = 'app.wsgi.dev.application'
