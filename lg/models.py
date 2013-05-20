from django.db import models

# Create your models here.
class LivingGroup(models.Model):
    year = models.IntegerField('Yearbook year')
    lg_name = models.CharField('Living Group name', max_length = 60)
    rep_name = models.CharField("Representative's name", max_length = 60)
    rep_email = models.EmailField("Representative's email")
    rep_phone = models.CharField("Representative's phone number", max_length = 15)
    first_choice = models.DateTimeField('First time choice')
    second_choice = models.DateTimeField('Second time choice')
    third_choice = models.DateTimeField('Third time choice')
    alternative_choice = models.CharField('Alternative time', blank = True, max_length = 1000)
    location = models.CharField('Portrait location', blank = True, max_length = 1000)
    comments = models.CharField('Comments or concerns', blank = True, max_length = 1000)

    def __unicode__(self):
        return "%s : %s" %(self.year, self.lg_name)