from django import forms
from django.forms import ModelForm, SplitDateTimeField, widgets
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_unicode
from django.conf import settings

from lg.models import LivingGroup
from recaptcha.client import captcha

class ReCaptcha(widgets.Widget):
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY))

    def value_from_datadict(self, data, files, name):
        return [data.get(self.recaptcha_challenge_name, None), 
            data.get(self.recaptcha_response_name, None)]

class ReCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': (u'Invalid captcha')
    }

    def __init__(self, *args, **kwargs):
        self.widget = ReCaptcha
        self.required = True
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):
        super(ReCaptchaField, self).clean(values[1])
        recaptcha_challenge_value = smart_unicode(values[0])
        recaptcha_response_value = smart_unicode(values[1])
        check_captcha = captcha.submit(recaptcha_challenge_value,  recaptcha_response_value, settings.RECAPTCHA_PRIVATE_KEY, {})
        if not check_captcha.is_valid:
            raise forms.util.ValidationError(self.error_messages['captcha_invalid'])
        return values[0]
        
        
class LivingGroupForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = LivingGroup
        widgets = {
            'lg_name'           : forms.TextInput(           attrs = {'placeholder' : 'Example: Tau Nu Phi', 'size' : '30'}),
            'rep_name'          : forms.TextInput(           attrs = {'size' : '30'}),
            'rep_email'         : forms.TextInput(           attrs = {'size' : '30'}),
            'rep_phone'         : forms.TextInput(           attrs = {'size' : '30'}),
            'first_choice'      : forms.SplitDateTimeWidget (attrs = {'size' : '15'}, date_format = '%m/%d/%Y', time_format = '%I:%M%p'),
            'second_choice'     : forms.SplitDateTimeWidget (attrs = {'size' : '15'}, date_format = '%m/%d/%Y', time_format = '%I:%M%p'),
            'third_choice'      : forms.SplitDateTimeWidget (attrs = {'size' : '15'}, date_format = '%m/%d/%Y', time_format = '%I:%M%p'),
            'alternative_choice': forms.Textarea(            attrs = {'placeholder' : 'Example: We have study breaks on Thursday nights at 9pm.', 'cols': '60', 'rows':'4'}),
            'location'          : forms.Textarea(            attrs = {'placeholder' : 'Example: Outside our house on 84 Massachusetts Ave.', 'cols': '60', 'rows':'4'}),
            'comments'          : forms.Textarea(            attrs = {'placeholder' : 'Example: The outlet might far away, so bring a long extension cable.', 'cols': '60', 'rows':'4'}),
            'captcha'           : ReCaptcha()
        }
        exclude = ('year',)
    
    first_choice = SplitDateTimeField(input_date_formats = ['%m/%d/%Y'], input_time_formats = ['%I:%M%p'])
    second_choice = SplitDateTimeField(input_date_formats = ['%m/%d/%Y'], input_time_formats = ['%I:%M%p'])
    third_choice = SplitDateTimeField(input_date_formats = ['%m/%d/%Y'], input_time_formats = ['%I:%M%p'])
    captcha = ReCaptchaField();
