from .common import *


DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1','wachu']
# WSGI application
WSGI_APPLICATION = 'app.wsgi.prod.application'

import os
INSTALLED_APPS += ['storages'] 

STATICFILES_STORAGE = 'app.settings.storages.StaticS3Boto3Storage'
DEFAULT_FILE_STORAGE = 'app.settings.storages.MediaS3Boto3Storage'

#TODO S3 ACCESS ERROR 해결
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-1')