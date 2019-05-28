import os

from iipimage.storage import ImageStorage, image_storage
from mezzanine.conf import settings


class PersonalImageStorage(ImageStorage):
    '''
    An ImageStorsage class for the Personal Edition. Converts images to TIFF using Pillow instead of
    external utilities
    '''

    def _convert_image(self, name):
        """ Converts the image file at `name` to TIF """
        if settings.IMAGE_SERVER_EXT != 'tif':
            raise ValueError("Only conversion to tif is supported in the Personal Edition")

        full_path = self.path(name)
        dir_name, file_name = os.path.split(full_path)
        file_root, file_ext = os.path.splitext(file_name)
        tif_name = os.path.join(dir_name, '%s.tif' % file_root)

        from PIL import Image
        orig_image = Image.open(full_path)
        # Save image in TIF formate
        orig_image.save(tif_name)

        if tif_name != full_path:
            os.remove(full_path)


personal_image_storage = PersonalImageStorage()


# The personal edition uses its own image storage class. Server edition uses another.
# This function decides which instance to use - use it instead of iipimage.storage.image_storage.
def get_current_image_storage():
    if settings.PERSONAL_EDITION:
        return personal_image_storage
    else:
        return image_storage
