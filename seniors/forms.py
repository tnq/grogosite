from django import forms
from django.forms.formsets import formset_factory
from seniors.models import Senior, Activity
from django.forms import ModelForm

class SeniorForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Senior
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ex: Timothy Beaver IV'}),
            'name_comments': forms.Textarea(attrs={'placeholder': 'ex: Rene with an acute accent on the second e.'}),
            'sort_letter': forms.TextInput(attrs={'placeholder': 'B'}),
            'home_town': forms.TextInput(attrs={'placeholder': 'ex: Boston'}),
            'home_state_or_country': forms.TextInput(attrs={'placeholder': 'ex: Massachusetts (or U.K.)'}),
            
            'kerberos': forms.TextInput(attrs={'placeholder': 'ex: tim'}),
            'major': forms.TextInput(attrs={'placeholder': 'ex: 8 & 6 or 6-2 or 3'}),
            'lg': forms.TextInput(attrs={'placeholder': 'ex: First East, East Campus'}),
            'quote': forms.TextInput(attrs={'placeholder': 'ex: Science is a way of thinking much more than it is a body of knowledge.'}),
            'quote_author': forms.TextInput(attrs={'placeholder': 'ex: Carl Sagan'}),
        }
        exclude = ('tnq_year')

class ActivityForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Activity
        exclude = ('senior')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'ex: Underwater Basketweaving Society'}),
            'years': forms.TextInput(attrs={'placeholder': 'ex: 2 3 4'}),
            'offices': forms.TextInput(attrs={'placeholder': 'ex: Basketweaver-in-Chief'}),
        }

class KerberosForm (forms.Form):
    kerberos = forms.CharField(max_length=8)

ActivityFormSet = formset_factory(ActivityForm, extra=1)
