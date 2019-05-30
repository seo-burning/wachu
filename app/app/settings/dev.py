from .common import *

ALLOWED_HOSTS = ["localhost", "0.0.0.0", ".compute.amazonaws.com"]

DEBUG = True

# WSGI application
WSGI_APPLICATION = 'app.wsgi.dev.application'
