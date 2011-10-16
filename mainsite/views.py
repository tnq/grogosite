# Create your views here.
from django.shortcuts import render_to_response
from xml.etree import ElementTree
import urllib2
from email.utils import mktime_tz, parsedate_tz
from datetime import datetime

from django.core.cache import cache

def index(request):

    # Twitter
    tweet = cache.get("tweet")
    tweet_date = cache.get("tweet_date")
    if not tweet or not tweet_date:
        try:
            item = ElementTree.parse(urllib2.urlopen("http://twitter.com/statuses/user_timeline/56618461.rss")).find(".//item")
            tweet = item.findtext("title").replace("hrhgrogo: ", "")

            tweet_date = item.findtext("pubDate")
            tweet_date = mktime_tz(parsedate_tz(tweet_date))
            tweet_date = datetime.fromtimestamp(tweet_date)
            tweet_date = tweet_date.strftime("%e %b")
        except:
            tweet = "Error with Twitter!"
            tweet_date = "???"

        cache.set("tweet", tweet, 600)
        cache.set("tweet_date", tweet_date, 600)

    return render_to_response('tnq_site/index.html', {'tweet': tweet, 'tweet_date' : tweet_date })
