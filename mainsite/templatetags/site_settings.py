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
            value = "TAG %s NOT FOUND!" %(tag)
        else:
            value = ""
    return value

register.simple_tag(tnq_setting)    

@register.tag(name="evaluate")
def do_evaluate(parser, token):
    """
    tag usage {% evaluate object.textfield %}
    """
    try:
        tag_name, variable = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return EvaluateNode(variable)

class EvaluateNode(template.Node):
    def __init__(self, variable):
        self.variable = template.Variable(variable)

    def render(self, context):
        try:
            content = self.variable.resolve(context)
            t = template.Template(content)
            return t.render(context)
        except template.VariableDoesNotExist, template.TemplateSyntaxError:
            return 'Error rendering', self.variable

@register.filter
def in_group(user, group):
	"""Returns True/False if the user is in the given group(s).
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

	return filter(lambda x:x in user_groups, group_list)

in_group.is_safe = True
