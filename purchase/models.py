from django.db import models

# Create your models here.
class Book(models.Model):
    year = models.IntegerField(unique=True)
    original_inventory = models.IntegerField()
    current_inventory = models.IntegerField(editable=False)
    price = models.IntegerField(editable=False)
                
    def __unicode__(self):
	    return "%d (%d left, $%d)" % (self.year, self.current_number, self.price)

    class Meta:
        ordering = ['-year']