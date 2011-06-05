from django.contrib import admin
from scripts.purchase.models import Patron, Book

admin.site.register(Patron)
admin.site.register(Book)

