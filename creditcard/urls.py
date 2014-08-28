from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^graph/', 'creditcard.views.graph_dates', name='graph_dates'),
)
