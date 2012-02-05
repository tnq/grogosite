#!/usr/bin/python

import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage, get_connection

from mainsite.models import Setting
from seniors.models import Senior

class Command(BaseCommand):

    help = "Send email confirmations to all the current year's seniors in the database."

    def handle(self, *args, **options):

        tnq_year = Setting.objects.get(tag="tnq_year").value
        tnq_year = 2013
        photo_dir = settings.SENIOR_IMAGE_DIRECTORY

        if raw_input("This is going to send a LOT of emails to the %s seniors. Are you sure? [yN] " % tnq_year).lower() != "y":
            return
        if raw_input("Super sure? [yN] ").lower() != "y":
            return

        base_message = """Hi Senior!

Your friendly Technique staphers are busily laying out the Senior section of the yearbook, and we want to do one final check of your picture and data before we submit them.

This is it.  What appears below goes into the book, so please double- and triple-check everything to make sure we haven't made any mistakes.  Make especially sure to check the picture (it will be much higher quality in the book!)

For our sanity please don't ask us to make any major additions, but if your name is incorrect or we spelled something wrong please let us know immediately by emailing tnq-seniors@mit.edu.  Don't email us if everything is perfect.

Requisite plug: since you're appearing in this book, don't you want to have one to keep forever?  Order a copy at http://technique.mit.edu/buy/ ! </plug>

See you all at our book distribution in May!

--The Staph of Technique %s

P.S. Everyone who we think had their portrait taken should have recieved an email like this.  Obviously we can't tell if someone isn't on the list, so please ask all your senior friends to email us RIGHT NOW if they had their portrait taken and did not get this email.

Name as it will appear: %s
Picture: http://technique.mit.edu/static/seniorphotos/%s
Major: %s
Minor: %s
Home Town: %s
Home State (or Country): %s
"""

        connection = get_connection()
        connection.open()

        seniors = Senior.objects.filter(tnq_year=tnq_year).exclude(image_path=None)
        for senior in seniors:

            file_name = "%s-%s.jpg" % (senior.id, senior.kerberos)

            message = base_message % (tnq_year,
                             senior.name,
                             file_name,
                             senior.major,
                             senior.minor,
                             senior.home_town,
                             senior.home_state_or_country)

            if senior.lg:
                message += "\nLiving Group: %s" % senior.lg
            if senior.quote:
                message += "\nQuote: %s" % senior.quote
            if senior.quote_author:
                message += "\nQuote Author: %s" % senior.quote_author

            message += "\n"

            for activity in senior.activity_set.all():
                message += "\nActivity: %s" % activity.title
                if activity.years:
                    message += "\nYears: %s" % activity.years
                if activity.offices:
                    message += "\nOffices: %s" % activity.offices
                message += "\n"

            subject = "Technique %s Senior Information for %s" % (tnq_year, senior.name)
            recipient = ["%s@mit.edu" % senior.kerberos]
            bcc = ["tnq-seniors-info@mit.edu", "tnq.manboard+seniors@gmail.com"]
            sender = "tnq-seniors@mit.edu"
            email_message = EmailMessage(subject.encode("utf-8"), message.encode("utf-8"), sender, recipient, bcc, connection=connection)

            image_file = open(os.path.join(photo_dir,file_name), "rb")
            image = image_file.read()
            image_file.close()

            email_message.attach(file_name, image, 'image/jpeg')
            email_message.send()

            print "Sent message to %s" % senior.name

        connection.close()
