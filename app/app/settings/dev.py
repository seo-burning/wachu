from .common import *

ALLOWED_HOSTS += ['localhost']

DEBUG = True
INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
# WSGI application
WSGI_APPLICATION = 'app.wsgi.dev.application'
# SITE_ID = 2

INTERNAL_IPS = ('172.18.0.1',)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# INSTALLED_APPS += ['storages']

# STATICFILES_STORAGE = 'app.settings.storages.StaticS3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'app.settings.storages.MediaS3Boto3Storage'

# # TODO S3 ACCESS ERROR 해결
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-1')
