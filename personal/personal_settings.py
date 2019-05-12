# Link  ../digipal_project/local_settings.py here
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(
    sys.modules[os.environ['DJANGO_SETTINGS_MODULE']].__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'digipal',
    #     'USER': 'postgres',
    #     'PASSWORD': 'postgres',
    #     'HOST': '',
    #     'PORT': '',
    # },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'sqlite3.db'),
    }
}

DEBUG = True
COMPRESS_ENABLED = False

COMPRESS_PRECOMPILERS = (
    ('text/less', 'personal.compressor_filters.PrecompiledLessFilter'),
    ('text/typescript', 'personal.compressor_filters.PrecompiledTypescriptFilter'),
)

PRECOMPILED_STATIC_ROOT = os.path.join(PROJECT_DIR, 'precompiled-static')
CUSTOM_APPS = ['personal']

