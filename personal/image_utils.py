# This file contains various image utilities that are only used in the Personal Edition
#
# These utilities replace the IIPServer functionality in the Server Edition
from PIL import Image
from django.http import HttpResponse
from iipimage.storage import image_storage
from mezzanine.conf import settings


def get_iipimage_dimensions(iipimage):
    if not settings.PERSONAL_EDITION:
        return iipimage._get_image_dimensions()

    img = Image.open(image_storage.path(iipimage.name))
    return img.size


def get_image_thumbnail_url(image, height, width):
    if settings.PERSONAL_EDITION:
        url = '/personal/image/%d' % image.id
        if height is not None or width is not None:
            url += '?'
            if width:
                url += 'width=%d' % width
                if height:
                    url += '&'
            if height:
                url += 'height=%d' % height
        return url
    else:
        return image.iipimage.thumbnail_url(height, width)

def respond_with_image(iipimage, width=None, height=None):
    img = Image.open(image_storage.path(iipimage.name))
    size = img.size
    if width is None and height is None:
        width, height = size[0], size[1]
    if height is None:
        ratio = size[0] / width
        height = size[1] / ratio
    elif width is None:
        ratio = size[1] / height
        width = size[0] / ratio

    if width != size[0] or height != size[1]:
        img = img.resize((width, height))

    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response
