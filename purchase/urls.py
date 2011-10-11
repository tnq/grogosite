from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.core.urlresolvers import reverse


urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template' : 'tnq_site/buy.html'}, name='tnq_buy'),
    (r'^order/', redirect_to, {'url' : '/buy/' } ), #For some reason using "reverse('tnq_buy')" doesn't work here!
    
    url(r'^book/(?P<book_year>\d{4})/', 'purchase.views.buy_form', {'purchase_option':'book'}, name='buy_book'),
    url(r'^seniorbundle/', 'purchase.views.buy_form', {'purchase_option':'senior_bundle'}, name='buy_senior_bundle'),
    url(r'^freshmanbundle/', 'purchase.views.buy_form', {'purchase_option':'freshman_bundle'}, name='buy_freshman_bundle'),
    url(r'^patron/', 'purchase.views.buy_form', {'purchase_option':'patron'}, name='buy_patron'),
    
)
