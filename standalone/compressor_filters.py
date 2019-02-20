#
# The standalone version does not have node.js available, so it needs to precompile the less and ts files.
# This is taken care of by the precompile-static management command.
#
# However, dajngo-compressor still needs to access the precompiled files, instead of trying to compile them.
# We do this by these handle precompress compilers, which just return the new precompiled files.
#
from compressor.filters import FilterBase
from django.conf import settings
import os
import codecs


class PrecompiledFilter(FilterBase):
    def __init__(self, content, attrs, **kwargs):
        # attrs are passed so we must handle them
        super(PrecompiledFilter, self).__init__(content, **kwargs)

    source_extension = ''
    target_extension = ''

    def input(self, *args, **kwargs):
        basename = kwargs['basename']
        if not basename.endswith('.' + self.source_extension):
            raise ValueError('Bad compressor filter configuration, PrecompiledLessFilter cannot handle %s' % basename)
        basename = basename[:-len(self.source_extension)] + self.target_extension

        parts = basename.split('/')
        abs_path = os.path.join(settings.PRECOMPILED_STATIC_ROOT, *parts)

        with codecs.open(abs_path, encoding='utf-8') as f:
            content = f.read()
        return content


class PrecompiledLessFilter(PrecompiledFilter):
    def __init__(self, *args, **kwargs):
        super(PrecompiledLessFilter, self).__init__(*args, **kwargs)

    source_extension = 'less'
    target_extension = 'css'

class PrecompiledTypescriptFilter(PrecompiledFilter):
    def __init__(self, *args, **kwargs):
        super(PrecompiledTypescriptFilter, self).__init__(*args, **kwargs)

    source_extension = 'ts'
    target_extension = 'js'
