from django.db import models
from django.forms import ModelForm

# Create your models here.
class Book(models.Model):
    year = models.IntegerField()
    price = models.IntegerField()
    
    def __unicode__(self):
	return "%d ($%d)" % (self.year, self.price)

class Patron(models.Model):
    type = models.CharField(max_length = 10)
    color = models.CharField(max_length = 6)
    price = models.IntegerField()

    def __unicode__(self):
        return "%s - $%d (%d)" % (self.type, self.price, self.year)
