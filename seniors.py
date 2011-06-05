import csv
import os

reader = csv.DictReader(open('Seniors.csv', 'rU'))

string = """Hi Senior!

Your friendly Technique staphers are busily laying out the Senior section of the yearbook, and we want to do one final check of your picture and data before we submit them.  

This is it.  What appears below goes into the book, so please double- and triple-check everything to make sure we haven't made any mistakes.  Make especially sure to check the picture (it will be much higher quality in the book!)

For our sanity please don't ask us to make any major additions, but if your name is incorrect or we spelled something wrong please let us know immediately by emailing tnq-seniors@mit.edu.  Don't email us if everything is perfect.

Requisite plug: since you're appearing in this book, don't you want to have one to keep forever?  Order a copy at http://technique.mit.edu/buy/order/ ! </plug>

See you all at our book distribution in May!

--The Staph of Technique 2011

P.S. Everyone who we think had their portrait taken should have recieved an email like this.  Obviously we can't tell if someone isn't on the list, so please ask all your senior friends to email us RIGHT NOW if they had their portrait taken and did not get this email.

Name as it will appear: %s
Picture: http://technique.mit.edu/seniorphoto/%s
Major: %s
Minor: %s
Home Town: %s
Home State (or Country): %s
Living Group: %s
Quote: %s
Author: %s
Activity 1: %s
Years 1: %s
Offices 1: %s
Activity 2: %s
Years 2: %s
Offices 2: %s
Activity 3: %s
Years 3: %s
Offices 3: %s
Activity 4: %s
Years 4: %s
Offices 4: %s
"""

count = 0
for senior in reader:
    count = count + 1
    print (string % (senior['BOOKNAME'],
                     senior['NEWFILENAME'],
                     senior['MAJOR'],
                     senior['MINOR'],
                     senior['HOMETOWN'],
                     senior['HOMESTATE'],
                     senior['LG'],
                     senior['QUOTE'],
                     senior['AUTHOR'],
                     senior['ACTIVITY1'],
                     senior['YEAR1'],
                     senior['OFFICE1'],
                     senior['ACTIVITY2'],
                     senior['YEAR2'],
                     senior['OFFICE2'],
                     senior['ACTIVITY3'],
                     senior['YEAR3'],
                     senior['OFFICE3'],
                     senior['ACTIVITY4'],
                     senior['YEAR4'],
                     senior['OFFICE4']))
