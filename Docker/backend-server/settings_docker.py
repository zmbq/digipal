# This file is copied to /digipal/settings_docker.py and replaces the version that is there.
# The original version imports settings.py, so we do, to
from .settings import *

import os
import sys

DEBUG = True

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

# Image server configuration
IMAGE_URLS_RELATIVE = True

# NOT SECURE
# We have to do this for the case where we are running in a VM on Windows
# Windows > VBox > Docker container
# The VM IP is dynamically assigned so we can't put anything specific in here.
# We don't have that issue on Linux where Host and Container share the same IP
# and localhost can be used.
ALLOWED_HOSTS = ['*']

IMAGE_SERVER_HOST = 'localhost:6080'   # Must be the same as the ports entry in docker-compose.yml
IMAGE_SERVER_ROOT = os.environ['IMAGE_SERVER_ROOT']

# Ignore the errors Pycharm reports here, everything is imported from settings.py, which Pycharm does not see

make_path(IMAGE_SERVER_ROOT)
make_path(os.path.join(IMAGE_SERVER_ROOT, IMAGE_SERVER_UPLOAD_ROOT))
make_path(os.path.join(IMAGE_SERVER_ROOT, IMAGE_SERVER_ORIGINALS_ROOT))

IMAGE_SERVER_ZOOMIFY = 'http://%s%s?zoomify=%s/'
IMAGE_SERVER_PATH = '/iip/iipsrv.fcgi'
IMAGE_SERVER_URL = 'http://%s%s' % (IMAGE_SERVER_HOST, IMAGE_SERVER_PATH)

# Forwarded host (for proper nginx handling of redirects)
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
