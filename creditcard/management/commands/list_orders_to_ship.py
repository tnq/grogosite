#!/usr/bin/python

from django.core.management.base import BaseCommand, CommandError

from creditcard.models import LineItem
from mainsite.models import Setting

class Command(BaseCommand):

    def handle(self, *args, **options):
        tnq_year = Setting.objects.get(tag="tnq_year").value

        books = LineItem.objects.all().filter(year__lt=tnq_year)
        books = books.filter(deliverytype="n")
        books = books.filter(shipping_paid=True)

        if books:
            print "The following orders can be shipped today:"
            for book in books:
                print book