from django.db import models
from django.forms import ModelForm

# Create your models here.
class Book(models.Model):
    year = models.IntegerField()
    price = models.IntegerField()
    
    def __unicode__(self):
	return "%d ($%d)" % (self.year, self.price)

class Patron(Book):
    type = models.CharField(max_length = 10)
    color = models.CharField(max_length = 6)

    def __unicode__(self):
        return "%s - $%d (%d)" % (self.type, self.price, self.year)

#This model is not used to store any data!!! This is only used for the form,
#and the data is then passed to MIT's system via the request headers.    
class Purchaser(models.Model):
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    company = models.CharField(max_length = 50, blank=True, null=True)
    address1 = models.CharField(max_length = 50)
    address2 = models.CharField(max_length = 50, blank=True, null=True)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zip = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 50)

    ship_firstname = models.CharField(max_length = 50)	
    ship_lastname = models.CharField(max_length = 50)	
    ship_company = models.CharField(max_length = 50, blank=True, null=True)	
    ship_address1 = models.CharField(max_length = 50, blank=True, null=True)	
    ship_address2 = models.CharField(max_length = 50, blank=True, null=True)	
    ship_city = models.CharField(max_length = 50, blank=True, null=True)	
    ship_state = models.CharField(max_length = 50, blank=True, null=True)	
    ship_zip = models.CharField(max_length = 50, blank=True, null=True)	

class PurchaserForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Purchaser
