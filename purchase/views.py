# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.core.exceptions import ObjectDoesNotExist
from mainsite.models import Setting
from purchase.models import Book
      
def buy_form(request, purchase_option=None, book_year=None):

    #Pull these as request variables
    if not book_year:
        book_year = int(Setting.objects.get(tag="tnq_year").value)
        
    if purchase_option:
        option = purchase_option

    if option=="senior_bundle":
        #Add error handling here - what if this tag doesn't exist?
        shipping_price = Setting.objects.get(tag="bundle_shipping_price").value
        amount = Setting.objects.get(tag="senior_bundle_price").value
        
        order_tag = "%s-SeniorBundle" % book_year
        order_tag_pretty = "a Senior Bundle"
        
    elif option=="freshman_bundle":
        #Add error handling here - what if this tag doesn't exist?
        shipping_price = Setting.objects.get(tag="bundle_shipping_price").value
        amount = Setting.objects.get(tag="freshman_bundle_price").value
        
        order_tag = "%s-FreshmanBundle" % book_year
        order_tag_pretty = "a Freshman Bundle"
        
    elif option=="book":
        
        try:
            amount = Book.objects.get(year=book_year).price
        except ObjectDoesNotExist:
            return render_to_response('tnq_site/buy/book_not_available.html', {'book_year' : book_year })
            
        shipping_price = int(Setting.objects.get(tag="shipping_price").value)
        
        order_tag = "%s-Book" % book_year
        order_tag_pretty = "a copy of Technique %s" % book_year
        
    elif option=="patron":
        try:
            platinum_price = Setting.objects.get(tag="platinum_price").value
            gold_price = Setting.objects.get(tag="gold_price").value
            silver_price = Setting.objects.get(tag="silver_price").value
            bronze_price = Setting.objects.get(tag="bronze_price").value
            
            shipping_price = 0
        except ObjectDoesNotExist:
            pass
        
        return render_to_response('tnq_site/buy/patron_form.html', {'platinum_price' : platinum_price,
                                                                     'gold_price' : gold_price,
                                                                     'silver_price' : silver_price,
                                                                     'bronze_price' : bronze_price,
                                                                     'shipping_price' : 0,
                                                                     'book_year' : book_year })
    
    else:
        return HttpResponseRedirect(reverse('tnq_buy'))
        
    return render_to_response('tnq_site/buy/new_buy_form.html', {'order_tag' : order_tag,
                                                                 'order_tag_pretty' : order_tag_pretty,
                                                                 'amount' : amount,
                                                                 'shipping_price' : shipping_price })
