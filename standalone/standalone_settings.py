# Link  ../digipal_project/local_settings.py here
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(
    sys.modules[os.environ['DJANGO_SETTINGS_MODULE']].__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'digipal',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '',
    },
}

DEBUG = True
COMPRESS_ENABLED = False

COMPRESS_PRECOMPILERS = (
    ('text/less', 'standalone.compressor_filters.PrecompiledLessFilter'),
    ('text/typescript', 'standalone.compressor_filters.PrecompiledTypescriptFilter'),
)

PRECOMPILED_STATIC_ROOT = os.path.join(BASE_DIR, 'precompiled-static')
CUSTOM_APPS = ['standalone']

