# IPython log file

import csv
from seniors.models import Senior

photos = csv.DictReader(open("LifeTouchSeniors2.csv", "r"), fieldnames="id old_directory old_photo directory photo last first athena_name email".split())

rejects = csv.DictWriter(open("rejects2.csv", "w"), fieldnames=photos.fieldnames)

for photo in photos:
    kerberos = photo['email'].replace('@mit.edu', '')
    try:
        senior = Senior.objects.get(kerberos=kerberos, tnq_year=2012)
        senior.image_path = photo['directory'] + '/' + photo['photo']
        senior.save()
    except Senior.DoesNotExist:
        rejects.writerow(photo)
        
exit()
