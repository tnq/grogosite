from django.db import models

# Create your models here.
class Senior(models.Model):
    name = models.CharField('Your full name', max_length=50)
    name_comments = models.CharField('Please describe these accents in words', max_length=100, blank=True)
    sort_letter = models.CharField('First letter of your last name', max_length=1)
    tnq_year = models.IntegerField('Book Year')
    kerberos = models.CharField('Kerberos username', max_length=10, unique=True)
    major = models.CharField('Your major(s)', max_length=30)
    minor = models.CharField('Your minor(s)', max_length=30, blank=True)
    home_town = models.CharField('You hometown', max_length=50)
    home_state_or_country = models.CharField('Your home state (or country)', max_length=20)
    lg = models.CharField('Living group / dorm', max_length=30, blank=True)
    quote = models.CharField(max_length=300, blank=True)
    quote_author = models.CharField(max_length=50, blank=True, verbose_name="Quote source")
    image_path = models.CharField(max_length=40, null=True, verbose_name="Path to image file")

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.kerberos)

class Activity(models.Model):
    senior = models.ForeignKey(Senior)
    title = models.CharField('Name of group / activity', max_length=60, blank=True)
    years = models.CharField('Years involved', max_length=8, blank=True)
    offices = models.CharField('Offices held', max_length=100, blank=True)

    def __unicode__(self):
        return "Title: %s\nYears Involved:%s\nOffices:%s\n" % (self.title, self.years, self.offices)

    class Meta:
        verbose_name_plural = "Activities"


