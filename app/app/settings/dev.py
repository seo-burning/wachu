from .common import *

ALLOWED_HOSTS = ["wachu","localhost", "127.0.0.1", ".compute.amazonaws.com"]

DEBUG = True

# WSGI application
WSGI_APPLICATION = 'app.wsgi.dev.application'
