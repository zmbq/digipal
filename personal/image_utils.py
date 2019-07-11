# This file contains various image utilities that are only used in the Personal Edition
#
# These utilities replace the IIPServer functionality in the Server Edition
from PIL import Image
from django.http import HttpResponse
from mezzanine.conf import settings

from personal.storage import get_current_image_storage
from sendfile import sendfile

_image_storage = get_current_image_storage()

def get_iipimage_dimensions(iipimage):
    if not settings.PERSONAL_EDITION:
        return iipimage._get_image_dimensions()

    img = Image.open(_image_storage.path(iipimage.name))
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

def get_image_region_url(image, return_width, region_left, region_top, region_width, region_height):
    if settings.PERSONAL_EDITION:
        url = '/personal/image/%d/region/%d/%0.6f/%0.6f/%0.6f/%0.6f' % (
            image.id, return_width, region_top, region_left, region_width, region_height
        )
    else:
        url = settings.IMAGE_SERVER_RGN % \
                 (settings.IMAGE_SERVER_HOST, settings.IMAGE_SERVER_PATH, image.path(),
                  'WID=%d' % return_width,
                  region_left, region_top,
                  region_width, region_height)
    return url


def respond_with_image(request, iipimage, width=None, height=None):
    img_path = _image_storage.path(iipimage.name)
    img = Image.open(img_path)
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

    return sendfile(request, img_path)

def respond_width_image_region(iipimage, return_width, region_left, region_top, region_width, region_height):
    # region coordinates are relative - 0,0 is top left, 1,1 is bottom right
    img_path = _image_storage.path(iipimage.name)
    img = Image.open(img_path)
    size = img.size
    left = int(region_left * size[0])
    top = int(region_top * size[1])
    width = int(region_width * size[0])
    height = int(region_height * size[1])
    return_height = int(float(return_width) / width * height)

    region_image = img.crop((left, top, left + width, top + height))
    resized_region = region_image.resize((return_width, return_height))

    response = HttpResponse(content_type='image/png')
    resized_region.save(response, 'PNG')
    return response



