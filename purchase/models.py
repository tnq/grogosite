from django.db import models
from django import forms
from django.forms.formsets import formset_factory

# Create your models here.
class Book(models.Model):
    year = models.IntegerField()
    price = models.IntegerField()
    
    def __unicode__(self):
	    return "%d ($%d)" % (self.year, self.price)

    class Meta:
        ordering = ['-year']

class BookForm(forms.Form):
    numbers = forms.ChoiceField(choices=[(i,i) for i in range(1,5)])
    years = forms.ChoiceField(choices=
            [(book.year, "%s ($%s)"% (book.year, book.price)) for book in Book.objects.all().order_by("-year")])

BookFormSet = formset_factory(BookForm, extra=0)
