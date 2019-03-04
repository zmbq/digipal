from mezzanine.conf import settings

# Tell South about the iipimage field
# See
# http://south.readthedocs.org/en/latest/tutorial/part4.html#simple-inheritance
# from south.modelsinspector import add_introspection_rules
# add_introspection_rules([], ["^iipimage\.fields\.ImageField"])

# patch the iipimage to correct a bug (.image was hardcoded)
from iipimage.storage import *
from iipimage.fields import *

# Patch 3+1:
# We now support TIF as well as JP2 on the image server
# If default format is set to 'tif' then we overwrite the conversion instruction to a pyramidal TIF
# CONVERT_TO_JP2 = 'kdu_compress -i %s -o %s -rate -,4,2.34,1.36,0.797,0.466,0.272,0.159,0.0929,0.0543,0.0317,0.0185 Stiles="{1024,1024}" Cblk="{64,64}" Creversible=no Clevels=5 Corder=RPCL Cmodes=BYPASS'
if settings.IMAGE_SERVER_EXT == 'tif':
    from iipimage import storage
    storage.CONVERT_TO_JP2 = 'convert %s -define tiff:tile-geometry=256x256 -compress jpeg ptif:%s'

# PATCH 1:

# prefix the upload dir with IMAGE_SERVER_ADMIN_UPLOAD_DIR
generate_new_image_path_original = generate_new_image_path


def generate_new_image_path():
    ret = generate_new_image_path_original()
    # GN: prefix the path with settings.IMAGE_SERVER_ADMIN_UPLOAD_DIR
    try:
        import os
        ret = os.path.join(settings.IMAGE_SERVER_ADMIN_UPLOAD_DIR, ret)
        ret = ret[:-3] + settings.IMAGE_SERVER_EXT
    except Exception:
        pass
    return ret

# The name of the iipimage field was hardcoded.
# Changed to iipimage to match Page model.


def get_image_path(instance, filename):
    """Returns the upload path for a page image.

    The path returned is a Unix-style path with forward slashes.

    This filename is entirely independent of the supplied `name`. It
    includes a directory prefix of the first character of the UUID and
    a fixed 'jp2' extension.

    Note that the image that `name` is of is most likely not a JPEG
    2000 image. However, even though we're using a UUID, it's worth
    not futzing about with the possibility of collisions with the
    eventual filename. Also, it's more convenient to always be passing
    around the real filename.

    :param instance: the instance of the model where the ImageField is
      defined
    :type instance: `models.Model`
    :param filename: the filename that was originally given to the file
    :type filename: `str`
    :rtype: `str`

    """

    if instance.id:
        # Reuse the existing filename. Unfortunately,
        # instance.image.name gives the filename of the image being
        # uploaded, so load the original record.
        original = instance._default_manager.get(pk=instance.id)
        image_path = original.iipimage.name
        if not image_path:
            # While the model instance exists, it previously had no
            # image, so generate a new image path.
            image_path = generate_new_image_path()
        else:
            # The original image file must be deleted or else the save
            # will add a suffix to `image_path`.
            # GN: iipimage
            original.iipimage.delete(save=False)
    else:
        image_path = generate_new_image_path()

    return image_path

# PATCH 2:
# subprocess.check_call(shlex.split(command.encode('ascii')))
# Didn't work on Windows. Changed to a cross-platform implementation.


import os


def _call_image_conversion(command, input_path):
    """Run the supplied image conversion `command`.

    Tidy up by removing the original image at `input_path`.

    """
    print command, input_path
    try:
        # subprocess.check_call(shlex.split(command.encode('ascii')))
        os.system(command.encode('ascii'))
    except subprocess.CalledProcessError, e:
        os.remove(input_path)
        raise IOError('Failed to convert the page image to .jp2: %s' % e)
    finally:
        # Tidy up by deleting the original image, regardless of
        # whether the conversion is successful or not.
        os.remove(input_path)


image_storage._call_image_conversion = _call_image_conversion

# PATCH 4
# The image_storage accesses the image server to get the image dimensions. It uses settings.IMAGE_SERVER_URL by default.
# This is OK when the image server is on a different server entirely, or in the old Docker deployment, where everything
# is on the same server. It does not work in the new Docker deployment, where the image server is located in anotheer
# container.
# We need an internal URL for this, but only for getting the image dimensions.
# So, we change the storage URL just before calling _get_image_dimensions, and restore it afterwards. We know this
# works because Django is single threaded, and there's no async IO here, at all. So we don't expect a nasty race condition


def wrap_get_image_dimensions(old_function):
    def _wrapped(self):
        try:
            image_storage.base_url = settings.IMAGE_SERVER_INTERNAL_URL
            return old_function(self)
        finally:
            image_storage.base_url = settings.IMAGE_SERVER_URL

    return _wrapped


if hasattr(settings, 'IMAGE_SERVER_INTERNAL_URL'):
    ImageFieldFile._get_image_dimensions = wrap_get_image_dimensions(ImageFieldFile._get_image_dimensions)

