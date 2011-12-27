from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^graph/', 'creditcard.views.graph_dates', name='graph_dates'),
)
