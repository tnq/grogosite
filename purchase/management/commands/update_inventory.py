#!/usr/bin/python

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from mainsite.models import Setting
from purchase.models import Book, PriceLimit
from creditcard.models import LineItem

class Command(BaseCommand):

    def handle(self, *args, **options):        
        line_items = LineItem.objects.all().exclude(deliverytype = 'v')
        
        bought = {}
        for line_item in line_items:
            if line_item.year in bought:
                bought[line_item.year] += 1
            else:
                bought[line_item.year] = 1
        
        for year in sorted(bought):
            books = Book.objects.filter(year = year)
            if len(books):
                book = books[0]
                
                temp = book.current_inventory
                book.current_inventory = book.original_inventory - bought[year]                
                book.save()
                
                if temp != book.current_inventory:
                    print str(year) + " went from " + str(temp) + " books to " + str(book.current_inventory) + " books."

        for book in Book.objects.all():
            if int(Setting.objects.get(tag="preorder_active").value) and int(Setting.objects.get(tag="tnq_year").value) == book.year:
                amount = int(Setting.objects.get(tag="preorder_price").value)
            else:
                amount = int(Setting.objects.get(tag="base_price").value)
    
            price_limits = PriceLimit.objects.all()
            for price_limit in price_limits:
                if price_limit.upper_limit >= book.current_inventory:
                    amount = max(amount, price_limit.price)

            if book.price != amount:
                print str(book.year) + " went from $" + str(book.price) + " to $" + str(amount) + "."
                book.price = amount
                book.save()
            