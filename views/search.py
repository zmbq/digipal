from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.utils import simplejson
from digipal.models import *
from digipal.forms import GraphSearchForm, SearchPageForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

import logging
dplog = logging.getLogger('digipal_debugger')

def get_search_types():
    from content_type.search_hands import SearchHands
    from content_type.search_manuscripts import SearchManuscripts
    from content_type.search_scribes import SearchScribes
    #from content_type.search_graphs import SearchGraphs
    ret = [SearchManuscripts(), SearchHands(), SearchScribes()]
    #ret = [SearchScribes()]
    return ret

def get_search_types_display(content_types):
    ''' returns the content types as a string like this:
        'Hands', 'Scribes' or 'Manuscripts' 
    '''
    ret = ''
    for type in content_types:
        if ret:
            if type == content_types[-1]:
                ret += ' or '
            else:
                ret += ', '        
        ret += '\'%s\'' % type.label
    return ret

def record_view(request, content_type='', objectid='', tabid=''):
    context = {'tabid': tabid}
    
    # We need to do a search to show the next and previous record
    # Only when we come from the the search image.
    set_search_results_to_context(request, allowed_type=content_type, context=context)
    
    for type in context['types']:
        if type.key == content_type:
            context['id'] = objectid
            type.set_record_view_context(context, request)
            type.set_record_view_pagination_context(context, request)
            break
    
    template = 'pages/record_' + content_type +'.html'
    
    return render_to_response(template, context, context_instance=RequestContext(request))

def index_view(request, content_type=''):
    context = {}
    
    types = get_search_types()
    
    # search & sort
    from datetime import datetime
    t0 = datetime.now()
    for type in types:
        if type.key == content_type:
            type.set_index_view_context(context, request)
            break
    t1 = datetime.now()
    #print '%s' % (t1 - t0)
    
    # pagination
    page_letter = request.GET.get('pl', '').lower()
    context['pages'] = [{'label': 'All', 'id': '', 'selected': (not page_letter)}]
    context['selected_page'] = context['pages'][0]
    for i in range(ord('a'), ord('z') + 1):
        page = {'label': ('%s' % chr(i)).upper(), 'id': chr(i), 'selected': (chr(i) == page_letter), 'disabled': not(chr(i) in context['active_letters'])}
        context['pages'].append(page)
        if page['selected']:
            context['selected_page'] = page
    
    template = 'pages/record_index.html'
    
    return render_to_response(template, context, context_instance=RequestContext(request))

def search_image_view(request):
    images = Image.objects.all()
    
    from digipal.forms import FilterManuscriptsImages

    # Get Buttons
    context = {}

    context['view'] = request.GET.get('view', 'images')

    town_or_city = request.GET.get('town_or_city', '')
    repository = request.GET.get('repository', '')
    date = request.GET.get('date', '')

    # Applying filters
    if town_or_city:
        images = images.filter(item_part__current_item__repository__place__name = town_or_city)
    if repository:
        repository_place = repository.split(',')[0]
        repository_name = repository.split(', ')[1]
        images = images.filter(item_part__current_item__repository__name=repository_name,item_part__current_item__repository__place__name=repository_place)
    if date:
        images = images.filter(hands__assigned_date__date = date)

    images = images.filter(item_part_id__gt = 0)
    images = Image.sort_query_set_by_locus(images)

    context['images'] = images

    image_search_form = FilterManuscriptsImages()
    context['image_search_form'] = image_search_form
    context['query_summary'] = get_query_summary(request, '', True, [image_search_form])

    return render_to_response('digipal/image_list.html', context, context_instance=RequestContext(request))

def search_page_view(request):
    # Backward compatibility.
    #
    # Previously all the record pages would go through this search URL and view
    # and their URL was: 
    #     /digipal/search/?id=1&result_type=scribes&basic_search_type=hands&terms=Wulfstan
    # Now we redirect those requests to the record page
    #     /digipal/scribes/1/?basic_search_type=hands&terms=Wulfstan+&result_type=scribes
    qs_id = request.GET.get('id', '')
    qs_result_type = request.GET.get('result_type', '')
    if qs_id and qs_result_type:
        from django.shortcuts import redirect
        # TODO: get digipal from current project name or current URL
        redirect_url = '/%s/%s/%s/?%s' % ('digipal', qs_result_type, qs_id, request.META['QUERY_STRING'])
        return redirect(redirect_url)
    
    # Actually run the searches
    context = {}
    set_search_results_to_context(request, context=context, show_advanced_search_form=True)

    # check if the search was executed or not (e.g. form not submitted or invalid form)
    if context.has_key('results'):
        # Tab Selection Logic =
        #     we pick the tab the user has selected even if it is empty. END
        #     if none, we select a the advanced search content type
        #     if none or its result is empty we select the first non empty type 
        #     if none we select the first type. END
        result_type = request.GET.get('result_type', '')

        if not result_type:
            first_non_empty_type = None
            for type in context['types']:
                if type.key == context['search_type'] and not type.is_empty:
                    result_type = context['search_type']
                    break
                if not first_non_empty_type and not type.is_empty:
                    first_non_empty_type = type.key
            if not result_type: result_type = first_non_empty_type
        
        result_type = result_type or context['types'][0].key
        context['result_type'] = result_type
        
        # No result at all?
        for type in context['types']:
            if not type.is_empty:
                context['is_empty'] = False
        if context['is_empty']:
            context['search_help_url'] = get_cms_url_from_slug(getattr(settings, 'SEARCH_HELP_PAGE_SLUG', 'search_help'))

    # Initialise the advanced search forms 
    from django.utils import simplejson
    context['drilldownform'] = GraphSearchForm({'terms': context['terms'] or ''})
    
    custom_filters = get_search_page_js_data(context['types'], request.GET.get('from_link') in ('true', '1'))
    context['expanded_custom_filters'] = custom_filters['advanced_search_expanded'] 
    context['search_page_options_json'] = simplejson.dumps(custom_filters)
    for custom_filter in custom_filters['filters']:
        if custom_filter['key'] == context['search_type_defaulted']:
            context['filters_form'] = custom_filter
    
    from digipal.models import RequestLog
    RequestLog.save_request(request, sum([type.count for type in context['types']]))

    return render_to_response('search/search_page_results.html', context, context_instance=RequestContext(request))

def set_search_results_to_context(request, context={}, allowed_type=None, show_advanced_search_form=False):
    ''' Read the information posted through the search form and create the queryset
        for each relevant type of content (e.g. MS, Hand) => context['results']
        
        If the form was not valid or submitted, context['results'] is left undefined.
        
        Other context variables used by the search template are also set.        
    '''    
    
    # allowed_type: this variable is used to restrict the search to one content type only.
    # This is useful when we display a specific record page and we only
    # have to search for the related content type to show the previous/next links.
    #allowed_type = kwargs.get('allowed_type', None)
    #context = kwargs.get('context', {})
    
    context['terms'] = ''
    #context['submitted'] = ('basic_search_type' in request.GET) or ('terms' in request.GET)
    context['submitted'] = False
    # list of query parameter/form fields which can be changed without triggering a search 
    non_search_params = ['basic_search_type', 'from_link', 'result_type']
    for param in request.GET:     
        if param not in non_search_params and request.GET.get(param):
            context['submitted'] = True
    
    context['can_edit'] = has_edit_permission(request, Hand)
    context['types'] = get_search_types()
    context['search_types_display'] = get_search_types_display(context['types'])
    context['is_empty'] = True

    advanced_search_form = SearchPageForm(request.GET)
    
    advanced_search_form.fields['basic_search_type'].choices = [(type.key, type.label) for type in context['types']]
    if show_advanced_search_form:
        context['advanced_search_form'] = advanced_search_form

    if advanced_search_form.is_valid():
        # Read the inputs
        # - term
        term = advanced_search_form.cleaned_data['terms']
        context['terms'] = term or ' '
        context['query_summary'] = get_query_summary(request, term, context['submitted'], [type.form for type in context['types']])
        
        # - search type
        context['search_type'] = advanced_search_form.cleaned_data['basic_search_type']
        context['search_type_defaulted'] = context['search_type'] or context['types'][0].key
        
        if context['submitted']: 
            # Create the queryset for each allowed content type.
            # If allowed_types is None, search for each supported content type.
            for type in context['types']:
                if allowed_type in [None, type.key]:
                    context['results'] = type.build_queryset(request, term)

def get_query_summary(request, term, submitted, forms):
    # return a string that summarises the query
    ret = ''
    
    if submitted:
        if term.strip():
            ret = '"%s"' % term
        
        # Generate a dictionary with the form fields.
        # The key is the internal name of the field and the value is the display label 
        fields = {}
        for form in forms:
            for field_name in form.fields:
                field = form[field_name]
                # generate the display label
                # try, successively, the label, the empty_label then the initial value of the field
                fields[field_name] = getattr(field, 'label', '') or getattr(field.field, 'empty_label', '') or (field.field.initial) or field_name.title()
        
        # Transform the query string into a list of field label and their values             
        for param in request.GET:
            if param in fields:
                val = request.GET.get(param, '').strip()
                if val:
                    if ret:
                        ret += ', '
                    ret += '%s: "%s"' % (fields[param], val)
            
        if not ret.strip():
            ret = 'All'
            
    return ret

def get_search_page_js_data(content_types, expanded_search=False):
    filters = []
    for type in content_types:
        filters.append({
                         'html': type.form.as_ul(),
                         'label': type.label,
                         'key': type.key,
                         })        
    
    ret = {
        'advanced_search_expanded': expanded_search or any([type.is_advanced_search for type in content_types]),
        'filters': filters,
    };
    
    return ret

def get_cms_url_from_slug(slug):
    from mezzanine.pages.models import Page as MPage 
    for page in MPage.objects.filter(slug__iendswith='how-to-use-digipal'):
        return page.get_absolute_url()
    return u'/%s' % slug

def search_graph_view(request):
    """ View for Hand record drill-down """
    context = {}

    term = request.GET.get('terms', '').strip()
    script = request.GET.get('script_select', '')
    character = request.GET.get('character_select', '')
    allograph = request.GET.get('allograph_select', '')
    component = request.GET.get('component_select', '')
    feature = request.GET.get('feature_select', '')
    context['submitted'] = request.GET.get('submitted', '') or term or script or character or allograph or component or feature
    context['style']= 'allograph_list'
    context['term'] = term
    context['view'] = request.GET.get('view', 'images')
    
    context['drilldownform'] = GraphSearchForm()
    
    from datetime import datetime
    
    t0 = datetime.now()
    t4 = datetime.now()
    
    if context['submitted']:
        # .order_by('item_part__current_item__repository__name', 'item_part__current_item__shelfmark', 'descriptions__description','id')
        # Although we are listing hands on the front-end, we search for graphs and not for hand.
        # Two reasons: 
        #    searching for character and allograh at the same time through a Hand model would generate two separate joins to graph
        #        this would bring potentially invalid results and it is also much slower
        #    it is faster than excluding all the hands without a graph (yet another expensive join)
        #
        context['query_summary'] = get_query_summary(request, term, context['submitted'], [context['drilldownform']])
        
        if term:
            graphs = Graph.objects.filter(
                    Q(hand__descriptions__description__icontains=term) | \
                    Q(hand__scribe__name__icontains=term) | \
                    Q(hand__assigned_place__name__icontains=term) | \
                    Q(hand__assigned_date__date__icontains=term) | \
                    Q(hand__item_part__current_item__shelfmark__icontains=term) | \
                    Q(hand__item_part__current_item__repository__name__icontains=term) | \
                    Q(hand__item_part__historical_items__catalogue_number__icontains=term))
        else:
            graphs = Graph.objects.all()
            
        t1 = datetime.now()
        
        combine_component_and_feature = True
    
        wheres = []
        if script:
            graphs = graphs.filter(hand__script__name=script)
            context['script'] = Script.objects.get(name=script)
        if character:
            graphs = graphs.filter(
                idiograph__allograph__character__name=character)
            context['character'] = Character.objects.get(name=character)
        if allograph:
            graphs = graphs.filter(
                idiograph__allograph__name=allograph)
            context['allograph'] = Allograph.objects.filter(name=allograph)
        if component:
            wheres.append(Q(graph_components__component__name=component) | Q(idiograph__allograph__allograph_components__component__name=component))
            context['component'] = Component.objects.get(name=component)
        if feature:
            wheres.append(Q(graph_components__features__name=feature))
            context['feature'] = Feature.objects.get(name=feature)

        # ANDs all the Q() where clauses together
        if wheres:
            where_and = wheres.pop(0)
            for where in wheres:
                where_and = where_and & where    
            
            graphs = graphs.filter(where_and)
        
        t2 = datetime.now()
    
        # Get the graphs then id of all the related Hands
        # We use values_list because it is much faster, we don't need to fetch all the Hands at this stage
        # That will be done after pagination in the template
        # Distinct is needed here.
        graphs = graphs.distinct().order_by('hand__scribe__name', 'hand__id')
        #print graphs.query
        graph_ids = graphs.values_list('id', 'hand_id')
        
        # Build a structure that groups all the graph ids by hand id
        # context['hand_ids'] = [[1, 101, 102], [2, 103, 104]]
        # In the above we have two hands: 1 and 2. For hand 1 we have Graph 101 and 102.
        context['hand_ids'] = [[0]]
        last = 0
        for g in graph_ids:
            if g[1] != context['hand_ids'][-1][0]:
                context['hand_ids'].append([g[1]])
            context['hand_ids'][-1].append(g[0])
        del(context['hand_ids'][0])

        t3 = datetime.now()

        context['graphs_count'] = len(graph_ids)
        
        t4 = datetime.now()
        
        #print 'search %s; hands query: %s + graph count: %s' % (t4 - t0, t3 - t2, t4 - t3)
        
    t5 = datetime.now()
    
    ret = render_to_response(
        'pages/search_graph.html',
        context,
        context_instance=RequestContext(request))
    
    t6 = datetime.now()

    return ret

def search_suggestions(request):
    from digipal.utils import get_json_response
    from content_type.search_content_type import SearchContentType
    query = request.GET.get('q', '')
    try:
        limit = int(request.GET.get('l'))
    except:
        limit = 8
    suggestions = SearchContentType().get_suggestions(query)
    return get_json_response(suggestions)
