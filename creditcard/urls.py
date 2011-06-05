from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^graph/', 'scripts.creditcard.views.graph_dates', name='graph_dates'),
)
