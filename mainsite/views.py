from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from localflavor.us.forms import USPhoneNumberField
from django.core.cache import cache
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from datetime import datetime
from urllib2 import urlopen
from xml.etree import ElementTree
import tweepy

from checkout.models import User

class UserForm(forms.Form):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    kerberos = forms.CharField(label="Kerberos", required=True, max_length=8)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))
    phone = USPhoneNumberField(label="Phone Number", required=False)
    id_number = forms.IntegerField(label="MIT ID Number", required=True)

    def clean_id_number(self):
        """Ensure that the MIT ID number is 9 digits long."""
        id_number = self.cleaned_data['id_number']
        if len(str(id_number)) != 9:
            raise forms.ValidationError("Your ID number must have 9 digits.")
        return id_number

def index(request):

    # Twitter
    tweet, tweet_date = cache.get("tweet", [None, None])
    if tweet is None:
        try:
            auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
            auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

            api = tweepy.API(auth)

            tweets = api.user_timeline(count=1, exclude_replies=True)

            tweet = tweets[0].text

            tweet_date = tweets[0].created_at
            tweet_date = tweet_date.strftime("%e %b")
        except:
            tweet = ""
            cache.set("tweet", ["", None], 60)
        else:
            cache.set("tweet", [tweet, tweet_date], 600)

    #Upcoming events
    events = cache.get("events")

    if events is None:
        try:
            events = []
            name_space = '{http://www.w3.org/2005/Atom}'
            event_elements = ElementTree.parse(urlopen("https://www.google.com/calendar/feeds/r28lcips84n5bqspuidk7fi4og%40group.calendar.google.com/public/full?futureevents=true")).findall(name_space+"entry")

            for element in event_elements:
                event = {}
                event['title'] = element.findtext(name_space+"title")
                event['content'] = element.findtext(name_space+"content")

                start_time = element.find("{http://schemas.google.com/g/2005}when").get("startTime")[:19]
                start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
                event['start_time_full'] = start_time
                event['start_time'] = start_time.strftime("%A, %B %e @%l:%M %p")

                event['url'] = element.find(name_space+"link").get('href')

                events.append(event)

            events.sort(key=lambda event:event['start_time_full'])

        except:
            events = []
            cache.set("events", [], 60)
        else:
            cache.set("events", events, 600)

    return render_to_response('tnq_site/index.html', {'tweet': tweet,
                                                      'tweet_date' : tweet_date,
                                                      'events' : events })

@login_required
def staph(request):
    return render_to_response('tnq_site/staph.html', {})

def user_on_manboard(user):
    if user:
        return user.groups.filter(name='Manboard').count() != 0
    return False

@login_required
@user_passes_test(user_on_manboard)
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User()
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.set_password(form.cleaned_data['password'])
            new_user.kerberos = form.cleaned_data['kerberos']
            new_user.username = form.cleaned_data['kerberos']
            new_user.phone = form.cleaned_data['phone']
            new_user.email = "%s@mit.edu" % form.cleaned_data['kerberos']
            new_user.barcode_id = form.cleaned_data['id_number']
            new_user.is_staff = True
            new_user.save()

            # Add the user to the "Authenticated" group so he can edit the Wiki
            authenticated = Group.objects.get(name="Authenticated")
            new_user.groups.add(authenticated)
            new_user.save()

            request.session['new_user_id'] = new_user.id
            return HttpResponseRedirect(reverse('tnq_add_user_success'))
    else:
        form = UserForm()

    context = {'form': form}
    context.update(csrf(request))

    return render_to_response('tnq_site/add_user.html', context )

@login_required
def add_user_success(request):
    if 'new_user_id' in request.session:
        try:
            new_user = User.objects.get(id=request.session['new_user_id'])
        except ObjectDoesNotExist:
            del request.session['new_user_id']
            return HttpResponseRedirect(reverse('tnq_add_user'))
    else:
        return HttpResponseRedirect(reverse('tnq_add_user'))

    return render_to_response('tnq_site/add_user_success.html',
                             {'new_user' : new_user},
                             context_instance=RequestContext(request))
