from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse


urlpatterns = patterns('',

    url(r'^$', 'purchase.views.buy_info', name='tnq_buy'),
    (r'^order/', RedirectView.as_view(url='/buy/')), #For some reason using "reverse('tnq_buy')" doesn't work here!
    
    url(r'^book/(?P<book_year>\d{4})/', 'purchase.views.buy_form', {'purchase_option':'book'}, name='buy_book'),
    url(r'^seniorbundle/(?P<book_year>\d{4})?', 'purchase.views.buy_form', {'purchase_option':'senior_bundle'}, name='buy_senior_bundle'),
    url(r'^freshmanbundle/', 'purchase.views.buy_form', {'purchase_option':'freshman_bundle'}, name='buy_freshman_bundle'),
    url(r'^patron/', 'purchase.views.patron_form', name='buy_patron'),
    
)
