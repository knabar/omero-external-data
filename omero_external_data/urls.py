
from django.conf.urls.defaults import patterns, url
import views


urlpatterns = patterns('django.views.generic.simple',

    url(r'^(?P<obj_dtype>\w+)/(?P<obj_id>[0-9]+)/$',
         views.index, name='omero_external_data_index' ),
    url(r'^datasource/(?P<obj_dtype>\w+)/(?P<obj_id>[0-9]+)/$',
         views.load_datasource, name='omero_external_data_load_datasource' ),

 )
