from django import forms
from django.forms.formsets import formset_factory
from seniors.models import Senior, Activity
from django.forms import ModelForm

class SeniorForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Senior
        exclude = ('tnq_year')

class ActivityForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Activity
        exclude = ('senior')

class KerberosForm (forms.Form):
    kerberos = forms.CharField(max_length=8)

ActivityFormSet = formset_factory(ActivityForm, extra=1)
