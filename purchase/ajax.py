from dajax.core import Dajax
from dajaxice.core import dajaxice_functions
from purchase.models import Book, BookForm, BookFormSet
import locale

locale.setlocale( locale.LC_ALL, "")

def update_purchase(request, form):
    dajax = Dajax()
    form = dict(map(lambda x: x.split("="),form.split("&")))
    formset = BookFormSet(form)
    
    items = []
    price = 0
    
    if formset.is_valid():
        for form in formset:
            num_books = int(form.cleaned_data['numbers'])
            book_year = form.cleaned_data['years']

            price += num_books * Book.objects.get(year=book_year).price    

            items.append("%sx%s-Book" %(num_books, book_year))
    
    price = locale.currency(price, grouping=True)

    dajax.assign('#total', 'value', price);
    dajax.assign('#merchantDefinedData4', 'value', ", ".join(items));

    return dajax.json()

dajaxice_functions.register(update_purchase)
