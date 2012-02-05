#!/usr/bin/python

import csv
from django.core.management.base import LabelCommand, CommandError

from mainsite.models import Setting
from seniors.models import Senior

class Command(LabelCommand):

    help = "Updates the image_path settings of the seniors in the specified CSV file."

    def handle_label(self, label, **options):
        tnq_year = Setting.objects.get(tag="tnq_year").value   
             
        photos = csv.DictReader(open(label, "r"), fieldnames="id old_directory old_photo directory photo last first athena_name email".split())

        rejects = csv.DictWriter(open("rejects.csv", "w"), fieldnames=photos.fieldnames)

        for photo in photos:
            kerberos = photo['email'].replace('@mit.edu', '')
            try:
                senior = Senior.objects.get(kerberos=kerberos, tnq_year=tnq_year)
                new_path = photo['directory'] + '/' + photo['photo']
                if senior.image_path != new_path:
                    print "Updating %s with new image path %s" % (senior.name, new_path)
                    senior.image_path = new_path
                    senior.save()
            except Senior.DoesNotExist:
                rejects.writerow(photo)