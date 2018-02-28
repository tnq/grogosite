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
        make_option('--end',
                    dest='end',
                    type='int',
                    default=0,
                    help='Number of days in the past to start'),
        make_option('--dump_csv',
                    dest='dump_csv',
                    action='store_true',
                    default=False,
                    help='Dump CSV to stdout'),
        )

    def handle(self, *args, **options):
        br = mechanize.Browser(factory=mechanize.RobustFactory())

        br.open(settings.TNQ_CC_URL)
        br.select_form(name="interfaceSetup")

        br["userName"] = settings.TNQ_CC_FIRST_USERNAME

        br.submit()

        br.select_form(name="interface")
        br["userName"] = settings.TNQ_CC_USERNAME
        br["password"] = settings.TNQ_CC_PASSWORD
        br["merchantId"] = [settings.TNQ_CC_MERCHANT_ID]

        end = datetime.datetime.now()-datetime.timedelta(days=options['end'])

        br["dateFrom"] = (end-datetime.timedelta(days=options['days'])).strftime("%m/%d/%Y")
        br["dateTo"] = end.strftime("%m/%d/%Y")

        br.submit(label="load")

        bs = br._factory._links_factory._bs
        status = bs.fetch('div', {'class': 'status'})
        if status:
            print status
        else:
            br.select_form(name="export")
            csv_response = br.submit(name="action")

            if options['dump_csv']:
                csv_response = csv_response.readlines()
                print ''.join(csv_response)

            reader = csv.DictReader(csv_response)
            returnlist = creditcard.views.create_orders_from_file(reader)

            if returnlist:
                print yaml.dump(returnlist)
