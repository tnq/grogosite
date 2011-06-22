from django import forms
from django.forms.formsets import formset_factory
from django.forms.widgets import RadioSelect
from purchase.models import Book

patron_choices = (("platinum", "platinum"),
                  ("gold", "gold"),
                  ("silver", "silver"),
                  ("bronze", "bronze"),
                 )

class OrderForm(forms.Form):
    patron = forms.ChoiceField(widget = RadioSelect, 
                                choices = patron_choices,
                                required = False)
    patron_name = forms.CharField(required = False)
    shipping = forms.BooleanField(required = False)

class OldBookForm(forms.Form):
    numbers = forms.ChoiceField(choices=[(i,i) for i in range(1,5)])
    years = forms.ChoiceField(choices=
            [(book.year, "%s ($%s)"% (book.year, book.price)) for book in Book.objects.all().order_by("-year")])


class PurchaserForm(forms.Form):
    billTo_firstName = forms.CharField(label="First Name")
    billTo_lastName = forms.CharField(label="Last Name")
    billTo_email = forms.EmailField(label="E-Mail")
    billTo_company = forms.CharField(label="Company")
    billTo_street1 = forms.CharField(label="Street")
    billTo_street2 = forms.CharField(label="Room / Apt")
    billTo_city = forms.CharField(label="City")
    billTo_state = forms.CharField(label="State")
    billTo_postalCode = forms.CharField(label="Zip Code")
    billTo_country = forms.CharField(label="Country")
    billTo_phoneNumber = forms.CharField(label="Phone Number")

    shipTo_first = forms.CharField(label="First Name")
    shipTo_last = forms.CharField(label="Last Name")
    shipTo_company = forms.CharField(label="Company")
    shipTo_street_1 = forms.CharField(label="Street")
    shipTo_street_2 = forms.CharField(label="Room / Apt")
    shipTo_city = forms.CharField(label="City")
    shipTo_state = forms.CharField(label="State")
    shipTo_zip = forms.CharField(label="Zip Code")


OldBookFormSet = formset_factory(OldBookForm, extra=0)
