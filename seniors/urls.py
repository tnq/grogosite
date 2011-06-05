from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    #Bring this one back next year!
    url(r'^$', 'scripts.seniors.views.enterinfo', name='enter-info'),
    #url(r'^$', 'scripts.seniors.views.closed', name='enter-info'),
    url(r'^submit/', 'scripts.seniors.views.enterinfo', name='submit-info'),
    url(r'^thanks', 'scripts.seniors.views.thanks', name='submit-success'),
    url(r'^email/', 'scripts.seniors.views.email', name="senior-email"),
    url(r'^email/submit/', 'scripts.seniors.views.email', name="submit-email"),
    url(r'^emailsent/', 'scripts.seniors.views.emailsent'),
    url(r'^noinfo/', 'scripts.seniors.views.noinfo'),
    #url(r'^vieworder/(?P<order_id>\d+)/$', 'scripts.creditcard.views.order_detail', name='view-order-detail'),



)
