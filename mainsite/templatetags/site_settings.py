from django import template
from django.conf import settings
from mainsite.models import Setting
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import SafeUnicode
import random
import re

register = template.Library()

def tnq_setting(tag):
    try:
        value = Setting.objects.get(tag=tag).value
    except ObjectDoesNotExist:
        if settings.DEBUG:
            value = "TAG %s NOT FOUND!" % (tag)
        else:
            value = ""
    return value

register.simple_tag(tnq_setting)    

@register.filter
def sample(value, arg):
    return random.sample(value, arg)

@register.filter
def in_group(user, group):
    """Return true if the user is in any of the the given groups.
    Usage::
        {% if user|in_group:"Friends" %}
        or
        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}
    You can specify a single group or comma-delimited list.
    No white space allowed.
    """

    if re.search(',', group):
        group_list = re.sub('\s+','',group).split(',')
    elif re.search(' ', group):
        group_list = group.split()
    else:
        group_list = [group]

    user_groups = []
    for group in user.groups.all():
        user_groups.append(str(group.name))

    return len([group for group in group_list if group in user_groups]) > 0

in_group.is_safe = True