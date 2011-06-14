# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from django.db.models import Q
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.forms.formsets import formset_factory
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from scripts.purchase.models import Book

class BookForm(forms.Form):
    numbers = forms.ChoiceField(choices=[(i,i) for i in range(1,5)])
    years = forms.ChoiceField(choices=
            [(book.year, "%s ($%s)"% (book.year, book.price)) for book in Book.objects.all().order_by("-year")])

BookFormSet = formset_factory(BookForm, extra=0)

def buy_form(request):
    if request.method == "POST":
        formset = BookFormSet(request.POST)
        for form in formset.forms:
            if form.is_valid():
                print form.cleaned_data
            else:
                print "Invalid form!"
                print form
    else:
        formset = BookFormSet()
    return render_to_response('purchase/buy_form.html', {'formset':formset })
