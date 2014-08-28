from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^$', 'checkout.views.view_equipment', name='view_equipment'),
)
