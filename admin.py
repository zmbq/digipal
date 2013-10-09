from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes import generic
from django.db.models import Avg, Max, Min, Count
from django import forms
from django.core.urlresolvers import reverse
from models import Allograph, AllographComponent, Alphabet, Annotation, \
        Appearance, Aspect, \
        CatalogueNumber, Category, Character, Collation, Component, County, \
        CurrentItem, \
        Date, DateEvidence, Decoration, Description, \
        Feature, Format, \
        Graph, GraphComponent, \
        Hair, Hand, HistoricalItem, HistoricalItemType, \
        Idiograph, IdiographComponent, Institution, InstitutionType, \
        HistoricalItemDate, \
        ItemOrigin, ItemPart, ItemPartType, ItemPartItem, \
        Language, LatinStyle, Layout, \
        Measurement, \
        Ontograph, OntographType, Owner, \
        Image, Person, Place, PlaceType, PlaceEvidence, Proportion, \
        Reference, Region, Repository, \
        Scribe, Script, ScriptComponent, Source, Status, MediaPermission, \
        StewartRecord, HandDescription, RequestLog
import reversion
import django_admin_customisations
from django.utils.safestring import mark_safe
import re

import logging
dplog = logging.getLogger( 'digipal_debugger')

#########################
#                       #
#   Advanced Filters    #
#                       #
#########################

class ImageAnnotationNumber(SimpleListFilter):
    title = ('Annotations')

    parameter_name = ('Annot')

    def lookups(self, request, model_admin):
        return (
            ('1', ('At least five annotations')),
            ('2', ('Fewer than five annotations')),
        )        

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.annotate(num_annot = Count('annotation__image__item_part')).exclude(num_annot__lt = 5)
        if self.value() == '2':
            return queryset.annotate(num_annot = Count('annotation__image__item_part')).filter(num_annot__lt = 5)
            

class ImageFilterNoItemPart(SimpleListFilter):
    title = 'Item Part'

    parameter_name = ('item_part')

    def lookups(self, request, model_admin):
        return (
            ('with', ('With Item Part')),
            ('without', ('Without Item Part')),
        )        

    def queryset(self, request, queryset):
        if self.value() == 'with':
            return queryset.filter(item_part_id__gt = 0).distinct()
        if self.value() == 'without':
            return queryset.exclude(item_part_id__gt = 0).distinct()

class ImageWithFeature(SimpleListFilter):
    title = ('Associated Features')

    parameter_name = ('WithFeat')

    def lookups(self, request, model_admin):
        return (
            ('yes', ('Has feature(s)')),
            ('no', ('No features')),
        )        

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(annotation__graph__graph_components__features__id__gt = 0).distinct()
        if self.value() == 'no':
            return queryset.exclude(annotation__graph__graph_components__features__id__gt = 0)
           
class ImageWithHand(SimpleListFilter):
    title = ('Associated Hand')

    parameter_name = ('WithHand')

    def lookups(self, request, model_admin):
        return (
            ('yes', ('Has Hand(s)')),
            ('no', ('No Hand')),
        )        

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(hand__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(hand__isnull=True).distinct()
           

class DescriptionFilter(SimpleListFilter):
    title = ('To Fix or Check')

    parameter_name = ('toFixOrCheck')

    def lookups(self, request, model_admin):
        return (
            ('toFix', ('Needs to be fixed')),
            ('toCheck', ('Needs to be checked')),
            ('goodlikethis', ('No needs to be checked or fixed')),
        )   

    def queryset(self, request, queryset):
        if self.value() == 'toFix':
            return queryset.filter(description__contains = "FIX")
        if self.value() == 'toCheck':
            return queryset.filter(description__contains = "CHECK")
        if self.value() == 'goodlikethis':
            q = queryset.exclude(description__contains = "CHECK")
            k = q.exclude(description__contains = "FIX")
            return k


class HistoricalItemDescriptionFilter(SimpleListFilter):
    title = ('To Fix or Check')

    parameter_name = ('toFixOrCheck')

    def lookups(self, request, model_admin):
        return (
            ('toFix', ('Needs to be fixed')),
            ('toCheck', ('Needs to be checked')),
            ('goodlikethis', ('No needs to be checked or fixed')),
        )   

    def queryset(self, request, queryset):
        if self.value() == 'toFix':
            return queryset.filter(description__description__contains = "FIX")
        if self.value() == 'toCheck':
            return queryset.filter(description__description__contains = "CHECK")
        if self.value() == 'goodlikethis':
            q = queryset.exclude(description__description__contains = "CHECK")
            k = q.exclude(description__description__contains = "FIX")
            return k

class HistoricalItemKerFilter(SimpleListFilter):
    title = ('Ker')

    parameter_name = ('ker')

    def lookups(self, request, model_admin):
        return (
            ('yes', ('Contains Ker')),
            ('no', ('Not contains Ker')),
        )   

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(description__description__contains = "Ker")
        if self.value() == 'no':
            return queryset.exclude(description__description__contains = "Ker")

class HistoricalItemGneussFilter(SimpleListFilter):
    title = ('Gneuss')

    parameter_name = ('gneuss')

    def lookups(self, request, model_admin):
        return (
            ('yes', ('Contains Gneuss Number')),
            ('no', ('Not contains Gneuss Number')),
        )   

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(catalogue_numbers__source__label='G.')
        if self.value() == 'no':
            return queryset.exclude(catalogue_numbers__source__label='G.')

class HandItempPartFilter(SimpleListFilter):
    title = ('numbers of ItemParts')

    parameter_name = ('morethanoneItemPart')

    def lookups(self, request, model_admin):
        return (
            ('yes', ('Has more than one Item Part')),
            ('no', ('Has not more than one Item Part')),
        )   

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return Hand.objects.filter(item_part__historical_items__in = HistoricalItem.objects.annotate(num_itemparts= Count('itempart')).filter(num_itemparts__gt='1'))
        if self.value() == 'no':
            return Hand.objects.filter(item_part__historical_items__in = HistoricalItem.objects.annotate(num_itemparts= Count('itempart')).exclude(num_itemparts__gt='1'))

class HandGlossNumFilter(SimpleListFilter):
    title = ('number of Glossing Hands')

    parameter_name = ('glosshandwithnum')

    def lookups(self, request, model_admin):
        return (
            ('yes', ('Has Num. Glossing hands')),
            ('no', ('Not has Num. Glossing hands')),
        )   

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return Hand.objects.filter(gloss_only=True).filter(num_glosses__isnull=False)
        if self.value() == 'no':
            return Hand.objects.filter(gloss_only=True).filter(num_glosses__isnull=True)

class HandGlossTextFilter(SimpleListFilter):
    title = ('has Glossing Text')

    parameter_name = ('glosshandwithtext')

    def lookups(self, request, model_admin):
        return (
            ('yes', ('Has Glossed Text')),
            ('no', ('Not has Glossed text')),
        )   

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return Hand.objects.filter(gloss_only=True).filter(glossed_text__isnull=False)
        if self.value() == 'no':
            return Hand.objects.filter(gloss_only=True).filter(glossed_text__isnull=True) 

#########################
#                       #
#        Forms          #
#                       #
#########################

class GraphForm(forms.ModelForm):

    class Meta:
        model = Graph    

    def __init__(self, *args, **kwargs):
        # Don't look into other pages for possible grouping graphs.
        # We know that both the containing (group) graph and the child graphs
        # belong to the same page.
        super(GraphForm, self).__init__(*args, **kwargs)
        object = getattr(self, 'instance', None)
        try:
            if object and object.annotation:
                group_field = self.fields['group']
                group_field._set_queryset(Graph.objects.filter(annotation__image=object.annotation.image).exclude(id=object.id))
        except Annotation.DoesNotExist:
            print 'ERROR'

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image    

    def __init__(self, *args, **kwargs):
        # we change the label of the default value for the media_permission 
        # field so it displays the actual permission on the repository object.
        #
        # We also add a link to the repository in the help message under the 
        # field
        super(ImageForm, self).__init__(*args, **kwargs)
        image = getattr(self, 'instance', None)
        permission_field = self.fields['media_permission']
        if image:
            # TODO: remove code duplication in the functions
            repository = image.get_repository()
            if repository:
                permission = repository.get_media_permission()
                repository_url = reverse("admin:digipal_repository_change", 
                                         args=[repository.id])
                permission_field.empty_label = 'Inherited: %s' % permission
                permission_field.help_text += ur'''<br/>To inherit from the 
                    default permission set in the 
                    <a target="_blank" href="%s">repository</a>, please 
                    select the first option.<br/>''' % repository_url

class RepositoryForm(forms.ModelForm):

    class Meta:
        model = Repository

    def __init__(self, *args, **kwargs):
        # we change the label of the default value for the media_permission 
        # field so it displays the actual permission (public/private)
        super(RepositoryForm, self).__init__(*args, **kwargs)
        self.fields['media_permission'].empty_label = '%s' % Repository.get_default_media_permission()


#########################
#                       #
#     Admin Tables      #
#     Visualization     #
#                       #
#########################


class OwnerInline(admin.StackedInline):
    model = Owner


class AllographComponentInline(admin.StackedInline):
    model = AllographComponent

    filter_horizontal = ['features']


class IdiographInline(admin.StackedInline):
    model = Idiograph

    filter_horizontal = ['aspects']


class AllographAdmin(reversion.VersionAdmin):
    model = Allograph

    search_fields = ['name', 'character']

    list_display = ['name', 'character', 'created', 'modified']
    list_display_links = list_display

    filter_horizontal = ['aspects']
    inlines = [AllographComponentInline, IdiographInline]


class AlphabetAdmin(reversion.VersionAdmin):
    model = Alphabet

    filter_horizontal = ['ontographs', 'hands']
    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class AnnotationAdmin(reversion.VersionAdmin):
    model = Annotation

    list_display = ['author', 'image', 'status', 'before', 'graph', 'after',
            'thumbnail', 'created', 'modified']
    list_display_links = ['author', 'image', 'status', 'before', 'graph',
            'after', 'created', 'modified']
    search_fields = ['vector_id', 'image__display_label',
            'graph__idiograph__allograph__character__name']
    list_filter = ['author__username', 'graph__idiograph__allograph__character__name']

class AppearanceAdmin(reversion.VersionAdmin):
    model = Appearance

    list_display = ['text', 'sort_order', 'created', 'modified']
    list_display_links = ['text', 'sort_order', 'created', 'modified']
    search_fields = ['text', 'description']


class AspectAdmin(reversion.VersionAdmin):
    model = Aspect

    filter_horizontal = ['features']
    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class CatalogueNumberAdmin(reversion.VersionAdmin):
    model = CatalogueNumber

    list_display = ['historical_item', 'source', 'number', 'created',
            'modified']
    list_display_links = ['historical_item', 'source', 'number', 'created',
            'modified']
    search_fields = ['source__name', 'number']


class CategoryAdmin(reversion.VersionAdmin):
    model = Category

    list_display = ['name', 'sort_order', 'created', 'modified']
    list_display_links = ['name', 'sort_order', 'created', 'modified']
    search_fields = ['name']


class AllographInline(admin.StackedInline):
    model = Allograph

    filter_horizontal = ['aspects']


class CharacterAdmin(reversion.VersionAdmin):
    model = Character

    filter_horizontal = ['components']
    inlines = [AllographInline]
    list_display = ['name', 'unicode_point', 'form', 'created', 'modified']
    list_display_links = ['name', 'unicode_point', 'form', 'created',
            'modified']
    search_fields = ['name', 'form']


class CollationAdmin(reversion.VersionAdmin):
    model = Collation

    list_display = ['historical_item', 'fragment', 'leaves', 'front_flyleaves',
            'back_flyleaves', 'created', 'modified']
    list_display_links = ['historical_item', 'fragment', 'leaves',
            'front_flyleaves', 'back_flyleaves',
            'created', 'modified']


class ComponentAdmin(reversion.VersionAdmin):
    model = Component

    filter_horizontal = ['features']
    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class CountyAdmin(reversion.VersionAdmin):
    model = County

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class ItemPartInline(admin.StackedInline):
    model = ItemPart

class ItemPartItemInline(admin.StackedInline):
    model = ItemPartItem
    
    verbose_name = 'Historical Item Part'


class CurrentItemAdmin(reversion.VersionAdmin):
    model = CurrentItem

    list_display = ['repository', 'shelfmark', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['repository__name', 'shelfmark', 'description']
    list_filter = ['repository']

    inlines = [ItemPartInline]
    filter_horizontal = ['owners']


class DateEvidenceInline(admin.StackedInline):
    model = DateEvidence


class DateAdmin(reversion.VersionAdmin):
    model = Date

    inlines = [DateEvidenceInline]
    list_display = ['sort_order', 'date', 'created', 'modified']
    list_display_links = ['sort_order', 'date', 'created', 'modified']
    search_fields = ['date']


class DateEvidenceAdmin(reversion.VersionAdmin):
    model = DateEvidence

    list_display = ['hand', 'date', 'reference', 'created', 'modified']
    list_display_links = ['hand', 'date', 'reference', 'created', 'modified']
    search_fields = ['date_description']


class DecorationAdmin(reversion.VersionAdmin):
    model = Decoration

    list_display = ['historical_item', 'illustrated', 'decorated',
            'illuminated', 'created', 'modified']
    list_display_links = ['historical_item', 'illustrated', 'decorated',
            'illuminated', 'created', 'modified']
    search_fields = ['description']


class DescriptionAdmin(reversion.VersionAdmin):
    model = Description

    list_display = ['historical_item', 'source', 'created', 'modified', 'description']
    list_display_links = ['historical_item', 'source', 'created', 'modified']
    search_fields = ['description']
    list_filter = [DescriptionFilter]

class FeatureAdmin(reversion.VersionAdmin):
    model = Feature

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class FormatAdmin(reversion.VersionAdmin):
    model = Format

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class GraphComponentInline(admin.StackedInline):
    model = GraphComponent

    filter_horizontal = ['features']


class GraphAdmin(reversion.VersionAdmin):
    form = GraphForm
    model = Graph

    filter_horizontal = ['aspects']
    inlines = [GraphComponentInline]
    list_display = ['idiograph', 'hand', 'created', 'modified']
    list_display_links = ['idiograph', 'hand', 'created', 'modified']


class HairAdmin(reversion.VersionAdmin):
    model = Hair

    list_display = ['label', 'created', 'modified']
    list_display_links = ['label', 'created', 'modified']
    search_fields = ['label']


class PlaceEvidenceInline(admin.StackedInline):
    model = PlaceEvidence


class ProportionInline(admin.StackedInline):
    model = Proportion

class HandDescriptionInline(admin.StackedInline):
    model = HandDescription

class HandFilterSurrogates(admin.SimpleListFilter):
    title = 'Surrogates'
    parameter_name = 'surrogates'
    
    def lookups(self, request, model_admin):
        return (
                    ('1', 'with surrogates'),
                    ('0', 'without surrogates'),
                )
    
    def queryset(self, request, queryset):
        from django.db.models import Q
        q = Q(surrogates__isnull=True) | Q(surrogates__exact='')
        if self.value() == '0':
            return queryset.filter(q)
        if self.value() == '1':
            return queryset.exclude(q)

class HandAdmin(reversion.VersionAdmin):
    model = Hand

    filter_horizontal = ['images']
    list_display = ['label', 'num', 'item_part', 'script', 'scribe',
            'assigned_date', 'assigned_place', 'created',
            'modified']
    list_display_links = list_display
    search_fields = ['id', 'label', 'num', 
            'em_title', 'label', 'item_part__display_label', 
            'display_note', 'internal_note']
    list_filter = [HandItempPartFilter, HandFilterSurrogates, HandGlossNumFilter, HandGlossTextFilter]

    inlines = [HandDescriptionInline, DateEvidenceInline, PlaceEvidenceInline, ProportionInline]
    #exclude = ('scragg_description', 'em_description', 'description', 'mancass_description')
    
class CatalogueNumberInline(admin.StackedInline):
    model = CatalogueNumber


class CategoryInline(admin.StackedInline):
    model = Category


class CollationInline(admin.StackedInline):
    model = Collation


class DecorationInline(admin.StackedInline):
    model = Decoration


class DescriptionInline(admin.StackedInline):
    model = Description


class ItemDateInline(admin.StackedInline):
    model = HistoricalItemDate


class ItemOriginInline(admin.StackedInline):
    model = ItemOrigin


class PartLayoutInline(admin.StackedInline):
    model = Layout
    exclude = ('historical_item', )    

class ItemLayoutInline(admin.StackedInline):
    model = Layout
    exclude = ('item_part', )    

class HistoricalItemAdmin(reversion.VersionAdmin):
    model = HistoricalItem

    search_fields = ['catalogue_number', 'date', 'name']
    list_display = ['catalogue_number', 'name', 'date', 'historical_item_type', 
                    'historical_item_format', 'created', 'modified']
    list_display_links = list_display
    list_filter = ['historical_item_type', HistoricalItemDescriptionFilter, HistoricalItemKerFilter, HistoricalItemGneussFilter]
    
    fieldsets = (
                (None, {'fields': ('catalogue_number', 'name', 'date', )}),
                ('Classifications', {'fields': ('historical_item_type', 'categories')}),
                ('Properties', {'fields': ('language', 'vernacular', 'neumed', 'hair', 'url')}),
                ('Owners', {'fields': ('owners',)}),
                ('Legacy', {'fields': ('legacy_id', 'legacy_reference',)}),
                ) 
    readonly_fields = ['catalogue_number']
    filter_horizontal = ['categories', 'owners']
    inlines = [ItemPartItemInline, CatalogueNumberInline, CollationInline,
            DecorationInline, DescriptionInline, ItemDateInline,
            ItemOriginInline, ItemLayoutInline]

class HistoricalItemTypeAdmin(reversion.VersionAdmin):
    model = HistoricalItemType

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class GraphInline(admin.StackedInline):
    model = Graph

    filter_horizontal = ['aspects']


class IdiographComponentInline(admin.StackedInline):
    model = IdiographComponent

    filter_horizontal = ['features']


class IdiographAdmin(reversion.VersionAdmin):
    model = Idiograph

    filter_horizontal = ['aspects']
    inlines = [IdiographComponentInline, GraphInline]
    list_display = ['allograph', 'scribe', 'created', 'modified']
    list_display_links = ['allograph', 'scribe', 'created', 'modified']
    search_fields = ['allograph__name']


class ScribeInline(admin.StackedInline):
    model = Scribe


class InstitutionAdmin(reversion.VersionAdmin):
    model = Institution

    inlines = [OwnerInline, ScribeInline]
    list_display = ['institution_type', 'name', 'founder', 'place', 'created',
            'modified']
    list_display_links = ['institution_type', 'name', 'founder', 'place',
            'created', 'modified']
    search_fields = ['name', 'place__name']


class InstitutionTypeAdmin(reversion.VersionAdmin):
    model = InstitutionType

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']

class ItemDateAdmin(reversion.VersionAdmin):
    model = HistoricalItemDate

    list_display = ['historical_item', 'date', 'created', 'modified']
    list_display_links = ['historical_item', 'date', 'created', 'modified']
    search_fields = ['evidence']


class ItemOriginAdmin(reversion.VersionAdmin):
    model = ItemOrigin

    list_display = ['content_type', 'content_object', 'historical_item',
            'created', 'modified']
    list_display_links = ['content_type', 'content_object', 'historical_item',
            'created', 'modified']
    search_fields = ['evidence']


class HandInline(admin.StackedInline):
    model = Hand

    filter_horizontal = ['images']


class ImageInline(admin.StackedInline):
    model = Image

    exclude = ['image']


class ItemPartAdmin(reversion.VersionAdmin):
    model = ItemPart

    list_display = ['historical_item', 'current_item', 'locus', 'type', 
            'created', 'modified']
    list_display_links = list_display
    search_fields = ['locus', 'display_label',
            'historical_items__display_label', 'type__name']
    list_filters = ('type',)

    fieldsets = (
                (None, {'fields': ('type',)}),
                ('This part is currently found in ...', {'fields': ('current_item', 'locus', 'pagination')}),
                ('It belongs (or belonged) to another part...', {'fields': ('group',)}),
                ('Owners', {'fields': ('owners',)}),
                ) 
    filter_horizontal = ['owners']
    inlines = [ItemPartItemInline, HandInline, ImageInline, PartLayoutInline]

class ItemPartTypeAdmin(reversion.VersionAdmin):
    model = ItemPartType

    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']

class LanguageAdmin(reversion.VersionAdmin):
    model = Language

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class LatinStyleAdmin(reversion.VersionAdmin):
    model = LatinStyle

    list_display = ['style', 'created', 'modified']
    list_display_links = ['style', 'created', 'modified']
    search_fields = ['style']


class LayoutAdmin(reversion.VersionAdmin):
    model = Layout

    list_display = ['historical_item', 'created', 'modified']
    list_display_links = ['historical_item', 'created', 'modified']
    search_fields = ['comments']


class MeasurementAdmin(reversion.VersionAdmin):
    model = Measurement

    inlines = [ProportionInline]
    list_display = ['label', 'created', 'modified']
    list_display_links = ['label', 'created', 'modified']
    search_fields = ['label']


class OwnerAdmin(reversion.VersionAdmin):
    model = Owner

    list_display = ['content_object', 'content_type', 'date', 'rebound', 'annotated', 'dubitable', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['evidence', 'institution__name', 'person__name']
    

class CharacterInline(admin.StackedInline):
    model = Character

    filter_horizontal = ['components']

class OntographAdmin(reversion.VersionAdmin):
    model = Ontograph

    list_display = ['name', 'ontograph_type', 'nesting_level', 'created', 'modified']
    list_display_links = ['name', 'ontograph_type', 'created', 'modified']
    list_editable = ['nesting_level']
    list_filter = ['ontograph_type', 'nesting_level']
    search_fields = ['name', 'ontograph_type']

    inlines = [CharacterInline]

class OntographTypeAdmin(reversion.VersionAdmin):
    model = OntographType

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class HandsInline(admin.StackedInline):
    model = Hand.images.through


class ImageAdmin(reversion.VersionAdmin):
    form = ImageForm

    exclude = ['image', 'caption']
    inlines = [HandsInline]
    list_display = ['id', 'item_part', 'get_locus_label', 'thumbnail_with_link', 
            'media_permission', 'created', 'modified',
            #'caption', 
            'iipimage']
    list_display_links = list_display
    search_fields = ['id', 'folio_side', 'folio_number', 
            'item_part__display_label', 'iipimage']
    
    list_filter = ["media_permission__label", ImageAnnotationNumber, ImageWithFeature, ImageWithHand, ImageFilterNoItemPart]
    
    actions = ['bulk_editing', 'bulk_natural_sorting']

    def bulk_editing(self, request, queryset):
        from django.http import HttpResponseRedirect
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('digipal.views.admin.image.image_bulk_edit') + '?ids=' + ','.join(selected) )
    bulk_editing.short_description = 'Bulk edit'
    
    def get_locus_label(self, obj):
        return obj.get_locus_label()
    get_locus_label.short_description = 'Locus' 

class PersonAdmin(reversion.VersionAdmin):
    model = Person

    inlines = [OwnerInline]
    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class InstitutionInline(admin.StackedInline):
    model = Institution


class PlaceTypeAdmin(reversion.VersionAdmin):
    model = PlaceType

    list_display = ['name', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name']


class PlaceAdmin(reversion.VersionAdmin):
    model = Place

    fieldsets = (
                (None, {'fields': ('name', 'type')}),
                ('Regions', {'fields': ('region', 'current_county', 'historical_county')}),
                ('Coordinates', {'fields': ('eastings', 'northings')}),
                ('Legacy', {'fields': ('legacy_id',)}),
                ) 
    inlines = [InstitutionInline, PlaceEvidenceInline]
    
    list_display = ['name', 'type', 'region', 'current_county',
            'historical_county', 'created', 'modified']
    list_display_links = list_display
    search_fields = ['name', 'type']
    list_filter = ['type__name']

class PlaceEvidenceAdmin(reversion.VersionAdmin):
    model = PlaceEvidence

    list_display = ['hand', 'place', 'reference', 'created', 'modified']
    list_display_links = ['hand', 'place', 'reference', 'created', 'modified']
    search_fields = ['place_description', 'evidence']


class ProportionAdmin(reversion.VersionAdmin):
    model = Proportion

    list_display = ['hand', 'measurement', 'created', 'modified']
    list_display_links = ['hand', 'measurement', 'created', 'modified']
    search_fields = ['description']


class ReferenceAdmin(reversion.VersionAdmin):
    model = Reference

    list_display = ['name', 'name_index', 'legacy_reference', 'created',
            'modified']
    list_display_links = ['name', 'name_index', 'legacy_reference', 'created',
            'modified']
    search_fields = ['name']


class RegionAdmin(reversion.VersionAdmin):
    model = Region

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class CurrentItemInline(admin.StackedInline):
    model = CurrentItem

class RepositoryAdmin(reversion.VersionAdmin):
    form = RepositoryForm

    inlines = [CurrentItemInline]
    list_display = ['name', 'short_name', 'place', 'created', 'modified']
    list_display_links = ['name', 'short_name', 'place', 'created', 'modified']
    search_fields = ['legacy_id', 'name', 'short_name', 'place__name']
    list_filter = ['media_permission__label']


class ScribeAdmin(reversion.VersionAdmin):
    model = Scribe

    filter_horizontal = ['reference']
    inlines = [HandInline, IdiographInline]
    list_display = ['name', 'date', 'scriptorium', 'created', 'modified']
    list_display_links = ['name', 'date', 'scriptorium', 'created', 'modified']
    search_fields = ['legacy_id', 'name', 'date']


class ScriptComponentInline(admin.StackedInline):
    model = ScriptComponent

    filter_horizontal = ['features']


class ScriptAdmin(reversion.VersionAdmin):
    model = Script

    filter_horizontal = ['allographs']
    inlines = [ScriptComponentInline]
    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class SourceAdmin(reversion.VersionAdmin):
    model = Source

    list_display = ['name', 'created', 'modified', 'label']
    list_display_links = ['name', 'created', 'modified', 'label']
    search_fields = ['name', 'label']


class StatusAdmin(reversion.VersionAdmin):
    model = Status

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']


class LogEntryAdmin(reversion.VersionAdmin):
    list_display = ['action_time', 'user', 'content_type', 'change_message',
            'is_addition', 'is_change', 'is_deletion']
    list_filter = ['action_time', 'user', 'content_type']
    ordering = ['-action_time']
    readonly_fields = ['user', 'content_type', 'object_id', 'object_repr',
            'action_flag', 'change_message']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # Returning False causes table to not show up in admin image
        return True

    def has_delete_permission(self, request, obj=None):
        return False

class MediaPermissionAdmin(reversion.VersionAdmin):
    list_display = ['label', 'display_message', 'is_private']
    ordering = ['label']

class StewartRecordFilterMatched(admin.SimpleListFilter):
    title = 'Match'
    parameter_name = 'matched'
    
    def lookups(self, request, model_admin):
        return (
                    ('1', 'matched'),
                    ('0', 'not matched'),
                )
    
    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(hands__id__gt=0).distinct()
        if self.value() == '0':
            return queryset.all().exclude(hands__id__gt=0).distinct()

class StewartRecordFilterLegacy(admin.SimpleListFilter):
    title = 'Legacy'
    parameter_name = 'legacy'
    
    def lookups(self, request, model_admin):
        return (
                    ('1', 'has legacy id'),
                    ('0', 'no legacy id'),
                )
    
    def queryset(self, request, queryset):
        from django.db.models import Q
        q = Q(stokes_db__isnull=True) | Q(stokes_db__exact='')
        if self.value() == '0':
            return queryset.filter(q)
        if self.value() == '1':
            return queryset.exclude(q)

class StewartRecordFilterMerged(admin.SimpleListFilter):
    title = 'Already Merged'
    parameter_name = 'merged'
    
    def lookups(self, request, model_admin):
        return (
                    ('1', 'yes'),
                    ('0', 'no'),
                )
    
    def queryset(self, request, queryset):
        from django.db.models import Q
        q = Q(import_messages__isnull=True) | Q(import_messages__exact='')
        if self.value() == '0':
            return queryset.filter(q)
        if self.value() == '1':
            return queryset.exclude(q)

class StewartRecordAdmin(reversion.VersionAdmin):
    model = StewartRecord
    
    list_display = ['id', 'field_hands', 'scragg', 'ker', 'gneuss', 'stokes_db', 'repository', 'shelf_mark']
    list_display_links = list_display
    list_filter = [StewartRecordFilterMatched, StewartRecordFilterLegacy, StewartRecordFilterMerged]
    search_fields = ['id', 'scragg', 'ker', 'gneuss', 'stokes_db', 'repository', 'shelf_mark']
    
    actions = ['match_hands', 'merge_matched']
    
    def field_hands(self, record):
        ret = ''
        for hand in record.hands.all():
            if ret: ret += ' ; '
            ret += u'Hand #%s' % hand.id
            ret += u', %s' % hand.scribe
            ret += u', %s' % hand.item_part
        return ret
    field_hands.short_description = 'Matched hand'

    def match_hands(self, request, queryset):
        from django.http import HttpResponseRedirect
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('digipal.views.admin.stewart.stewart_match') + '?ids=' + ','.join(selected) )
    match_hands.short_description = 'Match with DigiPal hand records'
    
    def merge_matched(self, request, queryset):
        from django.http import HttpResponseRedirect
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('digipal.views.admin.stewart.stewart_import') + '?ids=' + ','.join(selected) )
    merge_matched.short_description = 'Merge records into their matched hand records'
    
class RequestLogFilterEmpty(admin.SimpleListFilter):
    title = 'Result size'
    parameter_name = 'result_size'
    
    def lookups(self, request, model_admin):
        return (
                    ('0', 'empty'),
                    ('1', 'not empty'),
                )
    
    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(result_count__gt=0).distinct()
        if self.value() == '0':
            return queryset.filter(result_count=0).distinct()

class RequestLogAdmin(admin.ModelAdmin):
    model = RequestLog
    list_display = ['id', 'request_hyperlink', 'field_terms', 'result_count', 'created']
    list_display_links = ['id', 'field_terms', 'result_count', 'created']
    search_fields = ['id', 'request', 'result_count', 'created']
    ordering = ['-id']

    list_filter = [RequestLogFilterEmpty]

    def field_terms(self, record):
        return re.sub('^.*terms=([^&#?]*).*$', r'\1', record.request)
    field_terms.short_description = 'Terms'

    def request_hyperlink(self, record):
        ret = '<a href="%s">%s</a>' % (record.request, record.request)
        return ret
    request_hyperlink.short_description = 'Request'
    request_hyperlink.allow_tags = True
    
admin.site.register(Allograph, AllographAdmin)
admin.site.register(Alphabet, AlphabetAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Appearance, AppearanceAdmin)
admin.site.register(Aspect, AspectAdmin)
admin.site.register(CatalogueNumber, CatalogueNumberAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Collation, CollationAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(CurrentItem, CurrentItemAdmin)
admin.site.register(Date, DateAdmin)
admin.site.register(DateEvidence, DateEvidenceAdmin)
admin.site.register(Decoration, DecorationAdmin)
admin.site.register(Description, DescriptionAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Format, FormatAdmin)
admin.site.register(Graph, GraphAdmin)
admin.site.register(Hair, HairAdmin)
admin.site.register(Hand, HandAdmin)
admin.site.register(HistoricalItem, HistoricalItemAdmin)
admin.site.register(HistoricalItemType, HistoricalItemTypeAdmin)
admin.site.register(Idiograph, IdiographAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(InstitutionType, InstitutionTypeAdmin)
admin.site.register(HistoricalItemDate, ItemDateAdmin)
admin.site.register(ItemOrigin, ItemOriginAdmin)
admin.site.register(ItemPart, ItemPartAdmin)
admin.site.register(ItemPartType, ItemPartTypeAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(LatinStyle, LatinStyleAdmin)
admin.site.register(Layout, LayoutAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Ontograph, OntographAdmin)
admin.site.register(OntographType, OntographTypeAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PlaceType, PlaceTypeAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceEvidence, PlaceEvidenceAdmin)
admin.site.register(Proportion, ProportionAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Scribe, ScribeAdmin)
admin.site.register(Script, ScriptAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(MediaPermission, MediaPermissionAdmin)
admin.site.register(StewartRecord, StewartRecordAdmin)
admin.site.register(RequestLog, RequestLogAdmin)
