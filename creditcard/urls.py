from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^graph/', 'creditcard.views.graph_dates', name='graph_dates'),
)
