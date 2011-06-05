from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^$', 'scripts.purchase.views.buy_form', name='buy-form'),
    #url(r'^vieworder/(?P<order_id>\d+)/$', 'scripts.creditcard.views.order_detail', name='view-order-detail'),



)
