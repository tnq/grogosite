from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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
    (r'^orders/', include('scripts.creditcard.urls')),
    (r'^seniors/', include('scripts.seniors.urls')),
    url(r'^buy/', 'scripts.purchase.views.buy_form', name='buy_form'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/creditcard/purchaser/upload/$', 'scripts.creditcard.views.upload', name='upload'),
    (r'^%s/' % settings.DAJAXICE_URL_PREFIX, include('dajaxice.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(massadmin.massadmin.urls)),
    (r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login', name='login-page'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout-page'),
)

urlpatterns += staticfiles_urlpatterns()
