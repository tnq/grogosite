from django import template
from django.conf import settings
from mainsite.models import Setting
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import SafeUnicode
import random
import re

register = template.Library()

@register.simple_tag
def tnq_setting(tag):
    """Return the value of the tag, or a blank string if it does not exist."""
    try:
        value = Setting.objects.get(tag=tag).value
    except ObjectDoesNotExist:
        if settings.DEBUG:
            value = "TAG %s NOT FOUND!" % (tag)
        else:
            value = ""
    return value

@register.filter
def sample(population, k):
    """Return a list of k random samples from population."""
    return random.sample(population, k)

@register.filter
def in_group(user, groups):
    """Return the subset of "groups" to which the user belongs.
    Usage::
        {% if user|in_group:"Friends" %}
        or
        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}
    You can specify a single group or comma-delimited list.
    No white space allowed.
    """

    if re.search(',', groups):
        group_list = re.sub('\s+', '', groups).split(',')
    elif re.search(' ', groups):
        group_list = groups.split()
    else:
        group_list = [groups]

    user_groups = []
    for group in user.groups.all():
        user_groups.append(str(group.name))

    return [group for group in group_list if group in user_groups]

in_group.is_safe = True