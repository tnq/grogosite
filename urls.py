from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    (r'^orders/', include('scripts.creditcard.urls')),
    (r'^seniors/', include('scripts.seniors.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/creditcard/purchaser/upload/$', 'scripts.creditcard.views.upload', name='upload'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login', name='login-page'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout-page'),
    url(r'favicon\.gif$', 'django.views.generic.simple.redirect_to', {'url' : 'http://technique.mit.edu/static/favicon.gif'}),
    url(r'favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url' : 'http://technique.mit.edu/static/favicon.gif'}),
)
