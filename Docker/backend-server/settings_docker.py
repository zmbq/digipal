# Link  ../digipal_project/local_settings.py here
import os
import sys

def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

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

# Image server configuration
IMAGE_URLS_RELATIVE = True

# NOT SECURE
# We have to do this for the case where we are running in a VM on Windows
# Windows > VBox > Docker container
# The VM IP is dynamically assigned so we can't put anything specific in here.
# We don't have that issue on Linux where Host and Container share the same IP
# and localhost can be used.
ALLOWED_HOSTS = ['*']

# Remove this line to work with JP2 format
# Note that it requires a kakadu license for commercial applications
IMAGE_SERVER_EXT = 'tif'

IMAGE_SERVER_HOST = 'localhost'
IMAGE_SERVER_ROOT = '/images'

IMAGE_SERVER_UPLOAD_ROOT = 'jp2'
# python manage.py dpim will look under IMAGE_SERVER_ROOT +
# IMAGE_SERVER_ORIGINALS_ROOT for original images
IMAGE_SERVER_ORIGINALS_ROOT = 'originals'

make_path(IMAGE_SERVER_ROOT)
make_path(os.path.join(IMAGE_SERVER_ROOT, IMAGE_SERVER_UPLOAD_ROOT))
make_path(os.path.join(IMAGE_SERVER_ROOT, IMAGE_SERVER_ORIGINALS_ROOT))
IMAGE_SERVER_ADMIN_UPLOAD_DIR = os.path.join(
    IMAGE_SERVER_UPLOAD_ROOT, 'admin-upload')
make_path(IMAGE_SERVER_ADMIN_UPLOAD_DIR)

IMAGE_SERVER_ZOOMIFY = 'http://%s%s?zoomify=%s/'
IMAGE_SERVER_PATH = '/iip/iipsrv.fcgi'
IMAGE_SERVER_URL = 'http://%s%s' % (IMAGE_SERVER_HOST, IMAGE_SERVER_PATH)
