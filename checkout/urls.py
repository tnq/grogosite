from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'checkout.views.view_equipment', name='view_equipment'),
)
