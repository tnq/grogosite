from django.contrib import admin
from purchase.models import Book, PriceLimit

class BookAdmin(admin.ModelAdmin):
    list_display = ('year', 'current_inventory', 'price')
    readonly_fields = ('current_inventory','price')

admin.site.register(Book, BookAdmin)
admin.site.register(PriceLimit)

