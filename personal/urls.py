from django.conf.urls import patterns

urlpatterns = patterns('personal.views',
                       (r'^image/(?P<image_id>\d+)$', 'fetch_image'),
                       (r'^image/(?P<image_id>\d+)/region/(?P<return_width>\d+)/(?P<region_left>.*)/(?P<region_top>.*)/(?P<region_width>.*)/(?P<region_height>.*)', 'fetch_image_region')
)
