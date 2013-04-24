# Tell South about the iipimage field
# See http://south.readthedocs.org/en/latest/tutorial/part4.html#simple-inheritance
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^iipimage\.fields\.ImageField"])

# patch the iipimage to correct a bug (.image was hardcoded)
from iipimage import storage
from iipimage.storage import generate_new_image_path

import logging
dplog = logging.getLogger( 'digipal_debugger')

# PATCH 1:
# The name of the iipimage field was hardcoded.
# Changed to iipimage to match Page model.

def get_image_path (instance, filename):
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
            original.iipimage.delete(save=False)
    else:
        image_path = generate_new_image_path()
    return image_path

storage.get_image_path = get_image_path

# PATCH 2:
# subprocess.check_call(shlex.split(command.encode('ascii')))
# Didn't work on Windows. Changed to a cross-platform implementation.

import os

def _call_image_conversion (command, input_path):
    """Run the supplied image conversion `command`.

    Tidy up by removing the original image at `input_path`.

    """
    try:
        #subprocess.check_call(shlex.split(command.encode('ascii')))
        os.system(command.encode('ascii'))
    except subprocess.CalledProcessError, e:
        os.remove(input_path)
        raise IOError('Failed to convert the page image to .jp2: %s' % e)
    finally:
        # Tidy up by deleting the original image, regardless of
        # whether the conversion is successful or not.
        os.remove(input_path)

storage.image_storage._call_image_conversion = _call_image_conversion

from iipimage import fields

# Patch 3:
# The order of the query string arguments do matter, 
# if CVT appears before HEI, the resizing will fail on some iip image server implementations 

def thumbnail_url (self, height=None, width=None):
    try:
        height = '&HEI=%s' % str(int(height))
    except (TypeError, ValueError):
        height = ''
    try:
        width = '&WID=%s' % str(int(width))
    except (TypeError, ValueError):
        width = ''
    return '%s%s%s&CVT=JPEG' % (self.full_base_url, height, width)

fields.ImageFieldFile.thumbnail_url = thumbnail_url

# Patch 4:
# Fix Mezzanine case-insensitive keyword issue
# See https://github.com/stephenmcd/mezzanine/issues/647
from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.messages import error
# from django.contrib.comments.signals import comment_was_posted
# from django.core.urlresolvers import reverse
# from django.db.models import get_model, ObjectDoesNotExist
# from django.shortcuts import redirect
# from django.utils.translation import ugettext_lazy as _
# 
# from mezzanine.conf import settings
# from mezzanine.generic.fields import RatingField
# from mezzanine.generic.forms import ThreadedCommentForm

from django.http import HttpResponse, HttpResponseRedirect
from mezzanine.generic.models import Keyword, Rating

# from mezzanine.utils.cache import add_cache_bypass
# from mezzanine.utils.email import send_mail_template
# from mezzanine.utils.views import render, set_cookie, is_spam

@staff_member_required
def admin_keywords_submit(request):
    """
    Adds any new given keywords from the custom keywords field in the
    admin, and returns their IDs for use when saving a model with a
    keywords field.
    """
    ids, titles = [], []
    for title in request.POST.get("text_keywords", "").split(","):
        title = "".join([c for c in title if c.isalnum() or c in "- "])
        title = title.strip()
        if title:
            keywords = Keyword.objects.filter(title__iexact=title)
            
            # pick a case-sensitive match if it exists.
            # otherwise pick any other match.
            for keyword in keywords:
                if keyword.title == title:
                    break
            
            # no match at all, create a new keyword.
            if not keywords.count():
                keyword = Keyword(title=title)
                keyword.save()                
            
            id = str(keyword.id)
            if id not in ids:
                ids.append(id)
                titles.append(title)
    return HttpResponse("%s|%s" % (",".join(ids), ", ".join(titles)))

import mezzanine.generic.views
mezzanine.generic.views.admin_keywords_submit = admin_keywords_submit
