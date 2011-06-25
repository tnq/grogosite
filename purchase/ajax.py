from dajax.core import Dajax
from dajaxice.core import dajaxice_functions
from purchase.models import Book
from mainsite.models import Setting
from purchase.forms import OldBookFormSet, PurchaserForm, OrderForm
import locale

locale.setlocale( locale.LC_ALL, "")

def update_purchase(request, form):
    dajax = Dajax()
    form = dict(map(lambda x: x.split("="),form.split("&")))

    order_form = OrderForm(form, auto_id=False) 
    formset = OldBookFormSet(form)

    shipping_price = int(Setting.objects.get(tag="shipping_price").value)
    tnq_year = int(Setting.objects.get(tag="tnq_year").value)
    
    items = []
    price = 0

    if order_form.is_valid():
        shipping_paid = order_form.cleaned_data['shipping']
        senior_bundle = order_form.cleaned_data['senior_bundle']
        freshman_bundle = order_form.cleaned_data['freshman_bundle']
        patron = order_form.cleaned_data['patron']
        if patron:
            price += int(Setting.objects.get(tag="%s_price" %(patron)).value)
            items.append(patron.capitalize())
        if senior_bundle:
            price += int(Setting.objects.get(tag="bundle_price").value)
            if shipping_paid:
                price += 4 * shipping_price
            items.append("%s-Bundle"%(tnq_year))
        if freshman_bundle:
            price += int(Setting.objects.get(tag="bundle_price").value)
            if shipping_paid:
                price += 4 * shipping_price
            items.append("%s-Bundle"%(tnq_year+3))
    
    if formset.is_valid():
        for form in formset:
            num_books = int(form.cleaned_data['numbers'])
            book_year = form.cleaned_data['years']

            if num_books > 0:
                price += num_books * Book.objects.get(year=book_year).price    
                if shipping_paid:
                    price += num_books * shipping_price
                items.append("%sx%s-Book" %(num_books, book_year))
    
    price = locale.currency(price, grouping=True)
    items.sort(reverse=True)
    if shipping_paid:
        items.append("Shipping")
    items = ", ".join(items)

    dajax.assign('#total', 'value', price);
    dajax.assign('#comment', 'value', items);

    return dajax.json()

dajaxice_functions.register(update_purchase)
