# -*- coding: utf-8 -*-
# from digipal_text.models import *
from django.shortcuts import render
from django.utils.datastructures import SortedDict
from digipal import utils as dputils
from digipal_text.models import TextPattern
import regex as re
import logging
from digipal.utils import get_int_from_request_var
from django.db.utils import IntegrityError
from django.utils.text import slugify
dplog = logging.getLogger('digipal_debugger')

def patterns_view(request):

    from datetime import datetime

    t0 = datetime.now()

    # TODO: derive the info from the faceted_search settings.py or from a new
    # settings variable.
    from exon.customisations.digipal_text.models import Entry

    context = {}
    
    context['conditions'] = [
        {'key': '', 'label': 'May have'},
        {'key': 'include', 'label': 'Must have'},
        {'key': 'exclude', 'label': 'Must not have'},
        {'key': 'ignore', 'label': 'Ignore'},
    ]

    # arguments
    args = request.REQUEST
    context['units_limit'] = get_int_from_request_var(request, 'units_limit', 10)
    #context['units_range'] = args.get('units_range', '') or '25a1-62b2,83a1-493b3'
    context['units_range'] = args.get('units_range', '')

    context['wide_page'] = True

    # Update the patterns from the request
    update_patterns_from_request(request, context)

    # Get the text units
    context['units'] = []
    stats = {'response_time': 0, 'range_size': 0}

    for unit in Entry.objects.all():
        cx = unit.content_xml
        
        # only transcription
        if cx.id != 4: continue

        # only fief
        types = unit.get_entry_type()
        print unit.unitid, types
        if not types or 'F' not in types: continue

        # only selected range
        if not is_unit_in_range(unit, context['units_range']): continue
        
        stats['range_size'] += 1

        # segment the unit
        segment_unit(unit, context)

        if unit.match_conditions:
            context['units'].append(unit)

    # stats
    stats['result_size'] = len(context['units'])
    stats['result_size_pc'] = int(100.0 * stats['result_size'] / stats['range_size']) if stats['range_size'] else 'N/A'
    
    # limit size of returned result 
    if context['units_limit'] > 0:
        context['units'] = context['units'][0:context['units_limit']]

    stats['response_time'] = (datetime.now() - t0).total_seconds()
    context['stats'] = stats

    # render template
    template = 'digipal_text/patterns.html'
    if request.is_ajax():
        template = 'digipal_text/patterns_fragment.html'
    ret = render(request, template, context)

    return ret

def segment_unit(unit, context):
    patterns = context['patterns']
    unit.patterns = []
    
    unit.match_conditions = True
    
    for pattern_key, pattern in patterns.iteritems():
        if not pattern.id: continue
        if pattern.condition == 'ignore': continue
        
        # get regex from pattern
        rgx = get_regex_from_pattern(patterns, pattern_key)
        
        # apply regex to unit
        if rgx:
            found = False
            for match in rgx.finditer(unit.get_plain_content()):
                found = True
                unit.patterns.append([pattern_key, match.group(0)])
            if (pattern.condition == 'include' and not found) or (pattern.condition == 'exclude' and found):
                unit.match_conditions = False 
        
def get_regex_from_pattern(patterns, pattern_key):
    ret = None
    pattern = patterns.get(pattern_key, None)
    
    if pattern:
        ret = getattr(pattern, 'rgx', None)
        if ret is None:
            ret = pattern.pattern
            if ret:
                # <person> habet <number> mansionem
                ret = ret.replace(ur'<person>', ur'\w+')
                ret = ret.replace(ur'<number>', ur'\.?[ivxlcm]+\.?')
                print ret
                ret = pattern.rgx = re.Regex(ret)
    
    return ret

def update_patterns_from_request(request, context):
    # get patterns from DB as as sorted dictionary
    # {key: TextPattern}
    action = request.REQUEST.get('action', '')

    patterns = []
    fields = ['title', 'pattern', 'key', 'order', 'condition']
    for pattern in (list(TextPattern.objects.all()) + [TextPattern.get_empty_pattern()]):
        #print 'pattern #%s' % pattern.id
        pattern.condition = ''

        # modify the pattern from the request
        if action == 'update':
            modified = False
            for field in fields:
                value = request.REQUEST.get('p_%s_%s' % (pattern.id , field), '')
                if field == 'key' and value:
                    value = slugify(value)
                if value != getattr(pattern, field, ''):
                    #print '\t %s = %s' % (field, repr(value))
                    setattr(pattern, field, value)
                    if field != 'condition':
                        modified = True

            pattern.pattern = pattern.pattern.strip()
            if pattern.pattern:
                if modified:
                    print '\t SAVE'
                    try:
                        pattern.save()
                    except IntegrityError, e:
                        # title or key already used...
                        from datetime import datetime
                        pattern.title += ' (duplicate %s)' % datetime.now()
                        pattern.key += ' (duplicate %s)' % datetime.now()
                    except:
                        raise
            else:
                if pattern.id:
                    #print '\t DELETE'
                    pattern.delete()
                pattern = None

        # add the pattern to our list
        if pattern:
            patterns.append(pattern)

    # make sorted dict
    context['patterns'] = SortedDict()
    new_order = 0
    #print patterns
    patterns = sorted(patterns, key=lambda p: p.order)
    #print patterns
    for pattern in patterns:
        new_order += 1
        pattern.order = new_order
        context['patterns'][pattern.key] = pattern

    # add new dummy pattern so user can extend the list on the front-end
    pattern = TextPattern.get_empty_pattern()
    if pattern.key not in context['patterns']:
        context['patterns'][pattern.key] = pattern

def is_unit_in_range(unit, ranges):
    ret = False
    
    ranges = ranges.strip()
    
    if not ranges: return True

    unit_keys = dputils.natural_sort_key(unit.unitid)

    for range in ranges.split(','):
        parts  = range.split('-')
        if len(parts) == 2:
            ret = (unit_keys >= dputils.natural_sort_key(parts[0])) and (unit_keys <= dputils.natural_sort_key(parts[1]))
        else:
            ret = unit.unitid == parts[0]
        if ret: break

    return ret