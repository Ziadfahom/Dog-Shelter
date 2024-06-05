from .base import *

DEBUG = False

# List of allowed hosts
# Add 'EC2_PUBLIC_IP_ADDRESS' to the list of allowed hosts
ALLOWED_HOSTS = ['dogswatch.net', 'www.dogswatch.net', 'localhost', '127.0.0.1', '16.171.41.38']

SECURE_SSL_REDIRECT = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT')
    }
}

# Amazon S3 configurations for cloud storage. Use the .env file variables
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_DEFAULT_ACL = 'public-read'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{AWS_LOCATION}/'

DEFAULT_FILE_STORAGE = 'dogshelter_site.custom_storages.MediaStorage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/media/'

AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False  # Might want to adjust to True where URLs have signatures and expire after a certain time
