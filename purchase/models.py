from django.db import models

# Create your models here.
class Book(models.Model):
    year = models.IntegerField(unique=True)
    price = models.IntegerField()
    
    def __unicode__(self):
	    return "%d ($%d)" % (self.year, self.price)

    class Meta:
        ordering = ['-year']
