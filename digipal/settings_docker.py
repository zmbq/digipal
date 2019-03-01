# -*- coding: utf-8 -*-
from .settings import *

# Template file for local settings.
# Do NOT change settings.py instead copy this to local_settings.py, change it
# to suite the environment, but do NOT commit it to version control.
DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

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
IMAGE_SERVER_ROOT = os.path.join(PROJECT_ROOT, 'images')
IMAGE_SERVER_UPLOAD_ROOT = 'jp2'
IMAGE_SERVER_ORIGINALS_ROOT = 'originals'

make_path(IMAGE_SERVER_ROOT)
make_path(os.path.join(IMAGE_SERVER_ROOT, IMAGE_SERVER_UPLOAD_ROOT))
make_path(os.path.join(IMAGE_SERVER_ROOT, IMAGE_SERVER_ORIGINALS_ROOT))

IMAGE_SERVER_ZOOMIFY = 'http://%s%s?zoomify=%s/'
IMAGE_SERVER_PATH = '/iip/iipsrv.fcgi'
IMAGE_SERVER_URL = 'http://%s%s' % (IMAGE_SERVER_HOST, IMAGE_SERVER_PATH)

STATIC_ROOT = '/django/static'
make_path(STATIC_ROOT)

MEDIA_ROOT = '/django/media'
make_path(MEDIA_ROOT)

PROJECT_LOG_PATH = '/logs'
# Logging
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
            'level': DIGIPAL_LOG_LEVEL,
            'propagate': False,
        },
    },
}

