from django.db import models
from django.forms import ModelForm

# Create your models here.
class Senior(models.Model):
    name = models.CharField(max_length=50)
    name_comments = models.CharField(max_length=100, blank=True)
    sort_letter = models.CharField(max_length=1)
    tnq_year = models.IntegerField('Book Year')
    kerberos = models.CharField(max_length=10, unique=True)
    major = models.CharField(max_length=30)
    minor = models.CharField(max_length=30, blank=True)
    home_town = models.CharField('Home Town', max_length=50)
    home_state_or_country = models.CharField(max_length=20)
    lg = models.CharField('Living Group', max_length=30, blank=True)
    quote = models.CharField(max_length=300, blank=True)
    quote_author = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.kerberos)

class SeniorForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Senior
        exclude = ('tnq_year')

class Activity(models.Model):
    senior = models.ForeignKey(Senior)
    title = models.CharField('Activity Title', max_length=60, blank=True)
    years = models.CharField('Years Involved', max_length=8, blank=True)
    offices = models.CharField('Offices Held', max_length=100, blank=True)

    def __unicode__(self):
        return "Title: %s\nYears Involved:%s\nOffices:%s\n" % (self.title, self.years, self.offices)

    class Meta:
        verbose_name_plural = "Activities"

class ActivityForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Activity
        exclude = ('senior')
