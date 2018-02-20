import datetime

from django import forms
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

from mainsite.models import Setting
from purchase.models import Book

class BookForm(forms.Form):
    try:
        tnq_year = int(Setting.objects.get(tag="tnq_year").value)
    except ObjectDoesNotExist:
        # If the tag has not been defined, set it as one year past the current year
        tnq_year = datetime.datetime.now().year + 1
    year = forms.IntegerField(max_value=tnq_year, 
                              min_value=1885, 
                              required=False,
                              error_messages={'max_value' : "We haven't made that book yet!",
                                              'min_value' : "Technique didn't exist before 1885!",
                                              'invalid' : "Enter a whole number between 1885 and %s" % tnq_year})
    
def buy_info(request):
    if request.method == 'POST': #If the form has been submitted
        form = BookForm(request.POST)
        if form.is_valid() and form.cleaned_data['year']:
            return HttpResponseRedirect(reverse('buy_book', args=[form.cleaned_data['year']]))

    else:
        form = BookForm()

    context = {'form': form}
    context.update(csrf(request))

    return render_to_response('tnq_site/buy.html', context)
    
      
def buy_form(request, purchase_option=None, book_year=None):

    #Pull these as request variables
    if not book_year:
        book_year = int(Setting.objects.get(tag="tnq_year").value)

    one_shipping_price = int(Setting.objects.get(tag="shipping_price").value)
        
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
            book = Book.objects.get(year=book_year)
        except ObjectDoesNotExist:
            return render_to_response('tnq_site/buy/book_not_available.html', {'book_year' : book_year })
            
        if int(book.current_inventory) <= 0:
            return render_to_response('tnq_site/buy/book_not_available.html', {'book_year' : book_year })
            
        amount = book.price            
        shipping_price = one_shipping_price
        
        order_tag = "%s-Book" % book_year
        order_tag_pretty = "a copy of Technique %s" % book_year
            
    else:
        return HttpResponseRedirect(reverse('tnq_buy'))
        
    return render_to_response('tnq_site/buy/new_buy_form.html', {'order_tag' : order_tag,
                                                                 'order_tag_pretty' : order_tag_pretty,
                                                                 'amount' : amount,
                                                                 'shipping_price' : shipping_price,
                                                                 'one_shipping_price' : one_shipping_price})
                                                                 
def patron_form(request):
    try:
        platinum_price = Setting.objects.get(tag="platinum_price").value
        gold_price = Setting.objects.get(tag="gold_price").value
        silver_price = Setting.objects.get(tag="silver_price").value
        bronze_price = Setting.objects.get(tag="bronze_price").value
    
        shipping_price = 0
        book_year = str(Setting.objects.get(tag="tnq_year").value)
        
    except ObjectDoesNotExist:
        #Something needs to go here - at best the javascript will choke if there is no value,
        #and at worst it might allow sales of $0.
        pass

    return render_to_response('tnq_site/buy/patron_form.html', {'platinum_price' : platinum_price,
                                                                'gold_price' : gold_price,
                                                                'silver_price' : silver_price,
                                                                'bronze_price' : bronze_price,
                                                                'shipping_price' : 0,
                                                                'book_year' : book_year })
