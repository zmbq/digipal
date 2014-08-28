FACETED_SEARCH = {
    'types': [
                # label = the label displayed on the screen
                # label_col = the label in the column in the result table
                # type = the type of the field
                
                # path = a field name (can go through a related object or call a function)
                
                # count = True to show the number of hits for each possible value of the field (i.e. show facet options)
                # filter = True to let the user filter by this field
                # search = True if the field can be searched on (phrase query)
                # viewable = True if the field can be displayed in the result set
                
                # index = True iff (search or filter or count)
                
                # e.g. ann: viewable, full_size: count, repo_city: viewable+count+search
                # id: special
                # Most of the times viewable => searchable but not always (e.g. ann.)

                {
                    #'disabled': True,
                    'key': 'manuscript', 
                    'label': 'Manuscript',
                    'model': 'digipal.models.ItemPart',
                    'fields': [
                               
                               {'key': 'url', 'label': 'Address', 'label_col': ' ', 'path': 'get_absolute_url', 'type': 'url', 'viewable': True},
                               
                               {'key': 'hi_has_images', 'label_col': 'With images', 'label': 'With images', 'path': 'images.all.count', 'type': 'boolean', 'count': True},

                               {'key': 'hi_date', 'label': 'MS Date', 'path': 'historical_item.date', 'type': 'date', 'filter': True, 'viewable': True, 'search': True, 'id': 'hi_date', 'min': 500, 'max': 1300},
                               {'key': 'hi_index', 'label': 'Index', 'path': 'historical_item.catalogue_number', 'type': 'code', 'viewable': True, 'search': True},
                               {'key': 'hi_type', 'label': 'Type', 'path': 'historical_item.historical_item_type.name', 'type': 'code', 'viewable': True, 'count': True},
                               {'key': 'hi_format', 'label': 'Format', 'path': 'historical_item.historical_item_format.name', 'type': 'code', 'viewable': True, 'count': True},
                               {'key': 'repo_city', 'label': 'Repository City', 'path': 'current_item.repository.place.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                               {'key': 'repo_place', 'label': 'Repository Place', 'path': 'current_item.repository.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                               {'key': 'shelfmark', 'label': 'Shelfmark', 'path': 'current_item.shelfmark', 'search': True, 'viewable': True, 'type': 'code'},
                               {'key': 'locus', 'label': 'Locus', 'path': 'locus', 'search': True, 'viewable': True, 'type': 'code'},
                               {'key': 'hi_image_count', 'label_col': 'Images', 'label': 'Images', 'path': 'images.all.count', 'type': 'int', 'viewable': True},
                               #{'key': 'annotations', 'label_col': 'Ann.', 'label': 'Annotations', 'path': 'hands_set.all.count', 'type': 'int', 'viewable': True},
                               #{'key': 'thumbnail', 'label_col': 'Thumb.', 'label': 'Thumbnail', 'path': '', 'type': 'image', 'viewable': True, 'max_size': 70},
                               ],
                    'select_related': ['current_item__repository__place'],
                    'prefetch_related': ['historical_items', 'historical_items__historical_item_format', 'historical_items__historical_item_type', 'images'],
                    #'filter_order': ['hi_date', 'full_size', 'hi_type', 'hi_format', 'repo_city', 'repo_place'],
                    #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'annotations', 'hi_format', 'hi_type', 'thumbnail'],
                    'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_index', 'hi_date', 'hi_format', 'hi_type', 'hi_image_count'],
                    'sorted_fields': ['repo_city', 'repo_place', 'shelfmark', 'locus'],
                },

                {
                    #'disabled': True,
                    'key': 'image', 
                    'label': 'Image',
                    'model': 'digipal.models.Image',
                    'fields': [
                               
                               {'key': 'url', 'label': 'Address', 'label_col': ' ', 'path': 'get_absolute_url', 'type': 'url', 'viewable': True},
                               #{'key': 'scribe', 'label': 'Scribe', 'path': 'hands__scribes__count', 'faceted': True, 'index': True},
                               #{'key': 'annotation', 'label': 'Annotations', 'path': 'annotations__count01', 'faceted': True, 'index': True},
                               #
                               {'key': 'hi_date', 'label': 'MS Date', 'path': 'item_part.historical_item.date', 'type': 'date', 'filter': True, 'viewable': True, 'search': True, 'id': 'hi_date', 'min': 500, 'max': 1300},
                               {'key': 'img_is_public', 'label': 'Full Image', 'path': 'is_media_public', 'type': 'boolean', 'count': True, 'search': True},
                               {'key': 'hi_type', 'label': 'Type', 'path': 'item_part.historical_item.historical_item_type.name', 'type': 'code', 'viewable': True, 'count': True},
                               {'key': 'hi_format', 'label': 'Format', 'path': 'item_part.historical_item.historical_item_format.name', 'type': 'code', 'viewable': True, 'count': True},
                               {'key': 'repo_city', 'label': 'Repository City', 'path': 'item_part.current_item.repository.place.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                               {'key': 'repo_place', 'label': 'Repository Place', 'path': 'item_part.current_item.repository.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                               {'key': 'shelfmark', 'label': 'Shelfmark', 'path': 'item_part.current_item.shelfmark', 'search': True, 'viewable': True, 'type': 'code'},
                               {'key': 'locus', 'label': 'Locus', 'path': 'locus', 'search': True, 'viewable': True, 'type': 'code'},
                               {'key': 'annotations', 'label_col': 'Ann.', 'label': 'Annotations', 'path': 'annotation_set.all.count', 'type': 'int', 'viewable': True},
                               {'key': 'thumbnail', 'label_col': 'Thumb.', 'label': 'Thumbnail', 'path': '', 'type': 'image', 'viewable': True, 'max_size': 70},
                               ],
                    'select_related': ['item_part__current_item__repository__place'],
                    'prefetch_related': ['item_part__historical_items', 'item_part__historical_items__historical_item_format', 'item_part__historical_items__historical_item_type'],
                    'filter_order': ['hi_date', 'img_is_public', 'hi_type', 'hi_format', 'repo_city', 'repo_place'],
                    'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'annotations', 'hi_format', 'hi_type', 'thumbnail'],
                    #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date'],
                    'sorted_fields': ['repo_city', 'repo_place', 'shelfmark', 'locus'],
                    'views': [
                              {'icon': 'th-list', 'label': 'List', 'key': 'list'},
                              {'icon': 'th', 'label': 'Grid', 'key': 'grid', 'type': 'grid'},
                              ],
                },
    
                {
                    #'disabled': True,
                    'key': 'scribe', 
                    'label': 'Scribe',
                    'model': 'digipal.models.Scribe',
                    'fields': [
                               
                               {'key': 'url', 'label': 'Address', 'label_col': ' ', 'path': 'get_absolute_url', 'type': 'url', 'viewable': True},
                               
                               {'key': 'scribe', 'label': 'Scribe', 'path': 'name', 'type': 'title', 'viewable': True, 'search': True},

                               {'key': 'scribe_date', 'label': 'Scribe', 'path': 'date', 'type': 'date', 'viewable': True, 'filter': True, 'min': 500, 'max': 1300, 'id': 'scribe_date'},
                               
                               {'key': 'scriptorium', 'label': 'Scriptorium', 'path': 'scriptorium.name', 'type': 'title', 'viewable': True, 'search': True, 'count': True},
    
                               ],
                    #'select_related': ['item_part__current_item__repository__place'],
                    #'prefetch_related': ['item_part__historical_items', 'item_part__historical_items__historical_item_format', 'item_part__historical_items__historical_item_type'],
                    #'filter_order': ['hi_date', 'full_size', 'hi_type', 'hi_format', 'repo_city', 'repo_place'],
                    #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'annotations', 'hi_format', 'hi_type', 'thumbnail'],
                    #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date'],
                    'sorted_fields': ['scribe'],
                },

                {
                    #'disabled': True,
                    'key': 'hand', 
                    'label': 'Hand',
                    'model': 'digipal.models.Hand',
                    'fields': [
                               
                               {'key': 'url', 'label': 'Address', 'label_col': ' ', 'path': 'get_absolute_url', 'type': 'url', 'viewable': True},
                               
                               {'key': 'hand', 'label': 'Hand', 'path': 'get_search_label', 'type': 'title', 'viewable': True, 'search': True},
    
                               #{'key': 'full_size', 'label': 'Image', 'path': 'get_media_right_label', 'type': 'boolean', 'count': True, 'search': True},
                               #{'key': 'hi_type', 'label': 'Type', 'path': 'item_part.historical_item.historical_item_type.name', 'type': 'code', 'viewable': True, 'count': True},
                               #{'key': 'hi_format', 'label': 'Format', 'path': 'item_part.historical_item.historical_item_format.name', 'type': 'code', 'viewable': True, 'count': True},
                               {'key': 'repo_city', 'label': 'Repository City', 'path': 'item_part.current_item.repository.place.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                               {'key': 'repo_place', 'label': 'Repository Place', 'path': 'item_part.current_item.repository.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                               {'key': 'shelfmark', 'label': 'Shelfmark', 'path': 'item_part.current_item.shelfmark', 'search': True, 'viewable': True, 'type': 'code'},
                               {'key': 'hand_place', 'label': 'Place', 'path': 'assigned_place.name', 'search': True, 'viewable': True, 'type': 'code', 'count': True},
                               
                               {'key': 'hand_date', 'label': 'Date', 'path': 'assigned_date.date', 'type': 'date', 'filter': True, 'viewable': True, 'search': True, 'id': 'hi_date', 'min': 500, 'max': 1300},
                               
                               {'key': 'index', 'label': 'Index', 'path': 'item_part.historical_item.catalogue_number', 'search': True, 'viewable': True, 'type': 'code'},
                               
                               #{'key': 'locus', 'label': 'Locus', 'path': 'locus', 'search': True, 'viewable': True, 'type': 'code'},
                               #{'key': 'annotations', 'label_col': 'Ann.', 'label': 'Annotations', 'path': 'hands_set.all.count', 'type': 'int', 'viewable': True},
                               #{'key': 'thumbnail', 'label_col': 'Thumb.', 'label': 'Thumbnail', 'path': '', 'type': 'image', 'viewable': True, 'max_size': 70},
                               ],
                    'select_related': ['item_part__current_item__repository__place', 'assigned_place', 'assigned_date'],
                    'prefetch_related': ['item_part__historical_items'],
                    'filter_order': ['hand_date', 'repo_city', 'repo_place', 'hand_place'],
                    #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'annotations', 'hi_format', 'hi_type', 'thumbnail'],
                    #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date'],
                    'sorted_fields': ['hand', 'repo_city', 'repo_place', 'shelfmark'],
                },

                {
                    'disabled': False,
                    'key': 'graph', 
                    'label': 'Graph',
                    'model': 'digipal.models.Graph',
                    'django_filter': {'annotation__isnull': False},
                    'fields': [
                                {'key': 'url', 'label': 'Address', 'label_col': ' ', 'path': 'get_absolute_url', 'type': 'url', 'viewable': True},
    #                            {'key': 'hi_date', 'label': 'MS Date', 'path': 'item_part.historical_item.date', 'type': 'date', 'filter': True, 'viewable': True, 'search': True, 'id': 'hi_date', 'min': 500, 'max': 1300},
    #                            {'key': 'full_size', 'label': 'Image', 'path': 'get_media_right_label', 'type': 'boolean', 'count': True, 'search': True},
    #                            {'key': 'hi_type', 'label': 'Type', 'path': 'item_part.historical_item.historical_item_type.name', 'type': 'code', 'viewable': True, 'count': True},
    #                            {'key': 'hi_format', 'label': 'Format', 'path': 'item_part.historical_item.historical_item_format.name', 'type': 'code', 'viewable': True, 'count': True},
                                {'key': 'repo_city', 'label': 'Repository City', 'path': 'annotation.image.item_part.current_item.repository.place.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                                {'key': 'repo_place', 'label': 'Repository Place', 'path': 'annotation.image.item_part.current_item.repository.name', 'count': True, 'search': True, 'viewable': True, 'type': 'title'},
                                {'key': 'shelfmark', 'label': 'Shelfmark', 'path': 'annotation.image.item_part.current_item.shelfmark', 'search': True, 'viewable': True, 'type': 'code'},
                                {'key': 'locus', 'label': 'Locus', 'path': 'annotation.image.locus', 'search': True, 'viewable': True, 'type': 'code'},
    #                            {'key': 'annotations', 'label_col': 'Ann.', 'label': 'Annotations', 'path': 'annotation_set.all.count', 'type': 'int', 'viewable': True},
    #                            {'key': 'thumbnail', 'label_col': 'Thumb.', 'label': 'Thumbnail', 'path': '', 'type': 'image', 'viewable': True, 'max_size': 70},
    #                            {'key': 'script', 'label': 'Script', 'path': 'idiograph.allograh.script.name', 'viewable': True, 'type': 'code'},
                                {'key': 'chartype', 'label': 'Character Type', 'path': 'idiograph.allograph.character.ontograph.ontograph_type.name', 'viewable': True, 'type': 'code', 'count': True},
                                {'key': 'character', 'label': 'Character', 'path': 'idiograph.allograph.character.name', 'viewable': True, 'type': 'code', 'count': True},
                                {'key': 'allograph', 'label': 'Allograph', 'path': 'idiograph.allograph.name', 'viewable': True, 'type': 'code', 'count': True},
                               ],
                    'select_related': ['annotation__image__item_part__current_item__repository__place', 
                                       'idiograph__allograph__character__ontograph__ontograph_type', 
                                       ],
                    'prefetch_related': ['annotation__image__item_part__historical_items', 'annotation__image__item_part__historical_items__historical_item_format', 'annotation__image__item_part__historical_items__historical_item_type'],
                    'filter_order': ['repo_city', 'repo_place'],
                    #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date', 'annotations', 'hi_format', 'hi_type', 'thumbnail'],
                    #'column_order': ['url', 'repo_city', 'repo_place', 'shelfmark', 'locus', 'hi_date'],
                    'sorted_fields': ['repo_city', 'repo_place', 'shelfmark', 'locus'],
                    'views': [
                              {'icon': 'th-list', 'label': 'List', 'key': 'list'},
                              {'icon': 'th', 'label': 'Grid', 'key': 'grid', 'type': 'grid'},
                              ],
                }
            ]
}