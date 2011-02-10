import re

from django import template
from django.core.exceptions import ObjectDoesNotExist

from divensis.styling.models import Stylesheet


register = template.Library()

class StylesheetNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        try:
            relative_url = context['request'].get_full_path()
        except template.TemplateSyntaxError:
            # request context doesn't exist
            context[self.var_name] = "/* request context doesn't exist' */"
            return ''

        try:
            stylesheet = Stylesheet.objects.filter(url=relative_url)[:1].get().css
        except ObjectDoesNotExist:
            # no custom stylesheet in database
            context[self.var_name] = ""
            return ''

        context[self.var_name] = stylesheet
        return ''

@register.tag
def get_stylesheet_for_url(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]

    return StylesheetNode(var_name)
