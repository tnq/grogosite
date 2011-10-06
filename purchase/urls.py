from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^$', direct_to_template, {'template' : 'tnq_site/buy.html'}, name='tnq_buy'),
    url(r'^order/', 'purchase.views.buy_form', name='buy_form'),    
    
)
