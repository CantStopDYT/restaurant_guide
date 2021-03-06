from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sd#gg3p76^0qj-6%j8!htdr)j3q8$u3iq!!l6oj7t%dd5!fj)3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

DATABASES = {
    'default': {
         'ENGINE': 'django.contrib.gis.db.backends.postgis',
         'NAME': os.getenv('POSTGRES_NAME', 'resources'),
         'USER': os.getenv('POSTGRES_USER', 'resources'),
         'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'Pa55w0rD'),
         'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
         'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

on_heroku = 'DYNO' in os.environ
if on_heroku:
    import django_heroku
    import dj_database_url

    GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
    GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')

    os.environ['DATABASE_URL'] = os.environ['DATABASE_URL'].replace('postgres', 'postgis')
    # overwrite the default database
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

    # Activate Django-Heroku
    django_heroku.settings(locals())
