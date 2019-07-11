from django.shortcuts import get_object_or_404

from digipal.models import Image
from personal.image_utils import respond_with_image, respond_width_image_region


def fetch_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    try:
        width = int(request.GET['width'])
    except:
        width = None

    try:
        height = int(request.GET['height'])
    except:
        height = None

    response = respond_with_image(request, image.iipimage, width, height)
    return response

def fetch_image_region(request, image_id, return_width, region_left, region_top, region_width, region_height):
    image = get_object_or_404(Image, id=image_id)

    image_id = int(image_id)
    return_width = int(return_width)
    region_left = float(region_left)
    region_top = float(region_top)
    region_width = float(region_width)
    region_height = float(region_height)

    response = respond_width_image_region(image.iipimage, return_width, region_left, region_top, region_width, region_height)
    return response