from iipimage.fields import *
from django.conf import settings

# Patch 3:
# The order of the query string arguments do matter,
# if CVT appears before HEI, the resizing will fail on some iip image
# server implementations


def thumbnail_url(self, height=None, width=None):
    try:
        height = '&HEI=%s' % str(int(height))
    except (TypeError, ValueError):
        height = ''
    try:
        width = '&WID=%s' % str(int(width))
    except (TypeError, ValueError):
        width = ''

    return '%s%s%s&CVT=JPEG' % (self.full_base_url, height, width)
ImageFieldFile.thumbnail_url = thumbnail_url

# Patch:
# The ImageFieldFile uses the IIP server to get the image dimensions. This does not work in the new Docker
# environment, as the IIP server is not accessible from the backend docker container. We can add an internal
#def local_get_image_dimensions(self):
#    raise Exception("Overridden _get_image_dimensions called")
#ImageFieldFile._get_image_dimensions = local_get_image_dimensions


