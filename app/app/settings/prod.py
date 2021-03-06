from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk
import os
from .common import *


DEBUG = False
# WSGI application
WSGI_APPLICATION = 'app.wsgi.prod.application'

INSTALLED_APPS += ['storages']

STATICFILES_STORAGE = 'app.settings.storages.StaticS3Boto3Storage'
DEFAULT_FILE_STORAGE = 'app.settings.storages.MediaS3Boto3Storage'

# TODO S3 ACCESS ERROR 해결
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-1')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# s3 static settings
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


sentry_sdk.init(
    dsn="https://9dff4d52420943a0b2e17cdc1159eee5@o398991.ingest.sentry.io/5376553",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    # send_default_pii=True
)
