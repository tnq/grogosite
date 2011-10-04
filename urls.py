from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template, redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Dajaxice import
from dajaxice.core import dajaxice_autodiscover
from django.conf import settings
dajaxice_autodiscover()

import massadmin.massadmin

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^$', 'mainsite.views.index', name='tnq'),
    url(r'^beta/', 'mainsite.views.index', name='tnq_main'),
    (r'^orders/', include('creditcard.urls')),
    (r'^seniors/', include('seniors.urls')),
    (r'^equipment/', include('checkout.urls')),
    (r'^lg/', include('lg.urls')),
    (r'^buy/', include('purchase.urls')),
    url(r'^support/', direct_to_template, {'template' : 'tnq_site/support.html'}, name='tnq_support'),
    url(r'^join/', direct_to_template, {'template' : 'tnq_site/join.html'}, name='tnq_join'),
    url(r'^hire/', direct_to_template, {'template' : 'tnq_site/hire.html'}, name='tnq_hire'),
    
    #Favicon processing
    url(r'favicon\.ico/$', redirect_to, {'url' : settings.STATIC_URL + 'images/favicon.gif'}),
    url(r'favicon\.gif/$', redirect_to, {'url' : settings.STATIC_URL + 'images/favicon.gif'}),

    # Admin page
    (r'^admin/', include(massadmin.massadmin.urls)),
    (r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login', name='login-page'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout-page'),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/creditcard/purchaser/upload/$', 'creditcard.views.upload', name='upload'),
    (r'^%s/' % settings.DAJAXICE_URL_PREFIX, include('dajaxice.urls')),
    (r'^scripts/%s/' % settings.DAJAXICE_URL_PREFIX, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()
