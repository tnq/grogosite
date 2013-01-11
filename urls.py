from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template, redirect_to
import django.contrib.auth.views
from django.conf import settings
from django.contrib import admin
import massadmin.massadmin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^$', 'mainsite.views.index', name='tnq'),
    url(r'^beta/', 'mainsite.views.index', name='tnq_main'),
    url(r'^staph/$', 'mainsite.views.staph', name='tnq_staph'),
    url(r'^staph/user/$', 'mainsite.views.add_user', name='tnq_add_user'),
    url(r'^staph/user/success/$', 'mainsite.views.add_user_success', name='tnq_add_user_success'),
    (r'^orders/', include('creditcard.urls')),
    (r'^seniors/', include('seniors.urls')),
    (r'^equipment/', include('checkout.urls')),
    (r'^lg/', include('lg.urls')),
    (r'^buy/', include('purchase.urls')),
    (r'^wiki/', include('sapling.urls')),
    url(r'^support/', direct_to_template, {'template' : 'tnq_site/support.html'}, name='tnq_support'),
    url(r'^patrons/$', redirect_to, {'url' : '/support/'}),
    url(r'^join/', direct_to_template, {'template' : 'tnq_site/join.html'}, name='tnq_join'),
    url(r'^hire/', direct_to_template, {'template' : 'tnq_site/hire.html'}, name='tnq_hire'),
    url(r'^about/', direct_to_template, {'template' : 'tnq_site/about.html'}, name='tnq_about'),
    url(r'^archive/', direct_to_template, {'template' : 'tnq_site/archive.html'}, name='tnq_scans'),
    # Old Seniors page
    url(r'^scripts/seniors/?$', redirect_to, {'url' : '/seniors/info/'}),

    # Favicon processing
    url(r'favicon\.ico/$', redirect_to, {'url' : settings.STATIC_URL + 'images/favicon.gif'}),
    url(r'favicon\.gif/$', redirect_to, {'url' : settings.STATIC_URL + 'images/favicon.gif'}),

    # Admin page
    (r'^admin/', include(massadmin.massadmin.urls)),
    (r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login', name='login-page'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout-page'),

    # Password reset
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Orders uploading page
    url(r'^admin/creditcard/upload/$', 'creditcard.views.upload', name='orders_upload'),
)

urlpatterns += staticfiles_urlpatterns()
