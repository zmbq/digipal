from django.shortcuts import get_object_or_404

from digipal.models import Image
from personal.image_utils import respond_with_image


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

