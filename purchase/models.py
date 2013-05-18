from django.db import models
        
class PriceLimit(models.Model):
    upper_limit = models.IntegerField(unique=True, help_text = "When only this many books left, prices goes up")
    price = models.IntegerField(unique=True, help_text = "Price goes up to this value")
    
    def __unicode__(self):
        return "$%d for <= %d books" % (self.price, self.upper_limit)
        
        
class Book(models.Model):
    year = models.IntegerField(unique=True)
    original_inventory = models.IntegerField()
    current_inventory = models.IntegerField(default = 0)
    price = models.IntegerField(default = 0)
    
    def __unicode__(self):
	    return "%d" % self.year
                
    class Meta:
        ordering = ['-year']
