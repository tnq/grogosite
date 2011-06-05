from django.contrib import admin
from scripts.purchase.models import Purchaser, Patron, Book

admin.site.register(Purchaser)
admin.site.register(Patron)
admin.site.register(Book)

