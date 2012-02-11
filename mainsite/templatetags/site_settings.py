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

class TechniqueSettingNode(template.Node):
    def __init__(self, tag_name, var_name):
        self.tag_name = tag_name
        self.var_name = var_name

    def render(self, context):
        try:
            context[self.var_name] = Setting.objects.get(tag=self.tag_name).value
        except ObjectDoesNotExist:
            if settings.DEBUG:
                context[self.var_name] = "TAG %s NOT FOUND!" % (self.tag_name)
            else:
                context[self.var_name] = ""
        return ""

@register.tag(name="technique_setting")
def do_technique_setting(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    format_string, var_name = m.groups()
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return TechniqueSettingNode(format_string[1:-1], var_name)

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