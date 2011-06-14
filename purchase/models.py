from django.db import models
from django.forms import ModelForm

# Create your models here.
class Book(models.Model):
    year = models.IntegerField()
    price = models.IntegerField()
    
    def __unicode__(self):
	    return "%d ($%d)" % (self.year, self.price)

    class Meta:
        ordering = ['-year']
