# Create your views here.
from django.shortcuts import render_to_response
from xml.etree import ElementTree
from urllib2 import urlopen
from email.utils import mktime_tz, parsedate_tz
from datetime import datetime

from django.core.cache import cache

def index(request):

    # Twitter
    tweet, tweet_date = cache.get("tweet", [None, None])
    if tweet is None:
        try:
            item = ElementTree.parse(urlopen("http://twitter.com/statuses/user_timeline/56618461.rss")).find(".//item")
            tweet = item.findtext("title").replace("hrhgrogo: ", "")

            tweet_date = item.findtext("pubDate")
            tweet_date = mktime_tz(parsedate_tz(tweet_date))
            tweet_date = datetime.fromtimestamp(tweet_date)
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
            ns = '{http://www.w3.org/2005/Atom}'
            event_elements = ElementTree.parse(urlopen("https://www.google.com/calendar/feeds/r28lcips84n5bqspuidk7fi4og%40group.calendar.google.com/public/full?futureevents=true")).findall(ns+"entry")

            for element in event_elements:
                event = {}
                event['title'] = element.findtext(ns+"title")
                event['content'] = element.findtext(ns+"content")

                start_time = element.find("{http://schemas.google.com/g/2005}when").get("startTime")[:19]
                start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
                event['start_time'] = start_time.strftime("%A, %B %e @%l:%M %p")

                event['url'] = element.find("{http://www.w3.org/2005/Atom}link").get('href')

                events.append(event)
        except:
            events = []
            cache.set("events", [], 60)
        else:
            cache.set("events", events, 600)

    return render_to_response('tnq_site/index.html', {'tweet': tweet, 'tweet_date' : tweet_date, 'events' : events })
