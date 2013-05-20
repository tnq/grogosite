from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^$', direct_to_template, {'template' : 'tnq_site/lg.html'}, name='tnq_lg'),
    url(r'^signup/', 'lg.views.lgform', name='lg_signup'),
    url(r'^success/', direct_to_template, {'template' : 'tnq_site/lg/lg_success.html'}, name='lg_success'),
)
