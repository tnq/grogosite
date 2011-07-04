from django import template
from django.conf import settings
from scripts.mainsite.models import Setting
from django.core.exceptions import ObjectDoesNotExist

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
