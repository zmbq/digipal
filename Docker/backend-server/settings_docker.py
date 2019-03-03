# Link  ../digipal_project/local_settings.py here
import os
import sys

def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

PROJECT_DIR = os.path.dirname(os.path.abspath(
    sys.modules[os.environ['DJANGO_SETTINGS_MODULE']].__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

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

PROJECT_LOG_PATH = '/logs'

MEDIA_ROOT = '/django/media'
make_path(MEDIA_ROOT)
STATIC_ROOT = '/django/static'
make_path(STATIC_ROOT)

ANNOTATIONS_URL = 'uploads/annotations/'
ANNOTATIONS_ROOT = os.path.join(MEDIA_ROOT,
                                ANNOTATIONS_URL.strip('/'))

make_path(ANNOTATIONS_ROOT)

# Images uploads
UPLOAD_IMAGES_URL = 'uploads/images/'
UPLOAD_IMAGES_ROOT = os.path.join(MEDIA_ROOT,
                                  UPLOAD_IMAGES_URL.strip('/'))
make_path(UPLOAD_IMAGES_ROOT)

# Image cache
IMAGE_CACHE_URL = 'uploads/images/tmp/'
IMAGE_CACHE_ROOT = os.path.join(MEDIA_ROOT,
                                IMAGE_CACHE_URL.strip('/'))

make_path(IMAGE_CACHE_ROOT)

# Caches
DJANGO_CACHE_PATH = os.path.join('django', 'cache')
make_path(DJANGO_CACHE_PATH)
FILE_BASED_CACHE_BACKEND = 'digipal.middleware.FileBasedCacheArchetype'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'django-compressor': {
        'BACKEND': FILE_BASED_CACHE_BACKEND,
        'LOCATION': os.path.join(DJANGO_CACHE_PATH, 'django_compressor'),
        'TIMEOUT': 60 * 60 * 24,
        'MAX_ENTRIES': 300,
    },
    'digipal_faceted_search': {
        'BACKEND': FILE_BASED_CACHE_BACKEND,
        'LOCATION': os.path.join(DJANGO_CACHE_PATH, 'faceted_search'),
        'TIMEOUT': 60 * 60 * 24,
        # 'TIMEOUT': 1,
        'MAX_ENTRIES': 300,
    },
    'digipal_compute': {
        'BACKEND': FILE_BASED_CACHE_BACKEND,
        'LOCATION': os.path.join(DJANGO_CACHE_PATH, 'compute'),
        'TIMEOUT': 60 * 60 * 24,
        # 'TIMEOUT': 1,
        'MAX_ENTRIES': 300,
    },
    'digipal_text_patterns': {
        'BACKEND': FILE_BASED_CACHE_BACKEND,
        'LOCATION': os.path.join(DJANGO_CACHE_PATH, 'text_patterns'),
        'TIMEOUT': 60 * 60 * 24,
        # 'TIMEOUT': 1,
        'MAX_ENTRIES': 300,
    }
}

# Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'digipal_debug': {
            'format': '[%(asctime)s] %(levelname)s %(message)s (%(module)s)',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        # see digipal.utils.dplog()
        'digipal_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'digipal_debug',
            'filename': os.path.join(PROJECT_LOG_PATH, 'digipal.log'),
            'backupCount': 10,
            'maxBytes': 10 * 1024 * 1024,
        },
        'digipal_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'digipal_debug',
            'filename': os.path.join(PROJECT_LOG_PATH, 'error.log'),
            'backupCount': 10,
            'maxBytes': 10 * 1024 * 1024,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['digipal_error', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # see digipal.utils.dplog()
        'digipal_debugger': {
            'handlers': ['digipal_debug'],
            'level': DEBUG,
            'propagate': False,
        },
    },
}
