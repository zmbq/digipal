# Link  ../digipal_project/local_settings.py here
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(
    sys.modules[os.environ['DJANGO_SETTINGS_MODULE']].__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'digipal',
        'USER': 'app_digipal',
        'PASSWORD': 'dppsqlpass',
        'HOST': 'archetype-db',
        'PORT': '5432',
    },
}

#DEBUG = True
#COMPRESS_ENABLED = False

#COMPRESS_PRECOMPILERS = (
#    ('text/less', 'standalone.compressor_filters.PrecompiledLessFilter'),
#    ('text/typescript', 'standalone.compressor_filters.PrecompiledTypescriptFilter'),
#)

