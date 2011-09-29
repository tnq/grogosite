from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^$', 'checkout.views.view_equipment', name='view_equipment'),
)
