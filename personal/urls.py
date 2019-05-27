from django.conf.urls import patterns

urlpatterns = patterns('personal.views',
    (r'^image/(?P<image_id>\d+)$', 'fetch_image'),
)
