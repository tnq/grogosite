from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    #Bring this one back next year!
    url(r'^$', 'seniors.views.seniors', name='tnq_seniors'),
    url(r'^info/', 'seniors.views.enterinfo', name='enter_senior_info'),
    #url(r'^$', 'scripts.seniors.views.closed', name='enter-info'),
    url(r'^submit/', 'seniors.views.enterinfo', name='submit_senior_info'),
    url(r'^thanks', 'seniors.views.thanks', name='submit-success'),
    url(r'^email/', 'seniors.views.email', name="senior_email"),
    url(r'^email/submit/', 'seniors.views.email', name="submit-email"),
    url(r'^emailsent/', 'seniors.views.emailsent'),
    url(r'^noinfo/', 'seniors.views.noinfo'),
    #url(r'^vieworder/(?P<order_id>\d+)/$', 'scripts.creditcard.views.order_detail', name='view-order-detail'),



)
