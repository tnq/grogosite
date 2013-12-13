#!/usr/bin/python

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import creditcard.views

import csv
import datetime
import mechanize
import yaml
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--days',
                    dest='days',
                    type='int',
                    default=14,
                    help='Number of days to import orders from'),
        )

    def handle(self, *args, **options):
        br = mechanize.Browser(factory=mechanize.RobustFactory())

        br.open(settings.TNQ_CC_URL)
        br.select_form(name="interfaceForm")

        br["userName"] = settings.TNQ_CC_USERNAME

        br.submit()

        br.select_form(name="interfaceForm")
        br["password"] = settings.TNQ_CC_PASSWORD
        br["merchantId"] = settings.TNQ_CC_MERCHANT_ID

        br["dateFrom"] = (datetime.datetime.now()-datetime.timedelta(days=options['days'])).strftime("%m/%d/%Y")
        br["dateTo"] = datetime.datetime.now().strftime("%m/%d/%Y")

        br.submit(label="load")

        bs = br._factory._links_factory._bs
        status = bs.fetch('div', {'class': 'status'})
        if status:
            print status
        else:
            br.select_form(nr=0)
            csv_response = br.submit(name="export")

            reader = csv.DictReader(csv_response)
            returnlist = creditcard.views.create_orders_from_file(reader)

            if returnlist:
                print yaml.dump(returnlist)
