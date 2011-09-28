# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.forms.formsets import formset_factory
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from purchase.models import Book
from purchase.forms import OldBookFormSet

def buy_form(request):
    if request.method == "POST":
        formset = OldBookFormSet(request.POST)
        for form in formset.forms:
            if form.is_valid():
                print form.cleaned_data
            else:
                print "Invalid form!"
                print form
    else:
        formset = OldBookFormSet()
    return render_to_response('purchase/buy_form.html', {'formset':formset })
