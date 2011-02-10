import re

from django import template

from divensis.portfolio.models import Project, Category

register = template.Library()

@register.inclusion_tag('portfolio/render_project_details.html')
def render_project_details(details):
    lines = details.split("\n")
    regex = re.compile(r'\[(.+?)\]')
    result = []
    for line in lines:
        r = re.findall(regex, line)
        if len(r) == 2:
            type, content = r[0].strip(), r[1].strip()
            result.append({'type': type, 'content': content})
    return {'details': result}


class PortfolioCategories(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name
 
    def render(self, context):
        categories = Category.objects.all()
        context[self.var_name] = categories
        return ''
 
@register.tag
def get_portfolio_categories(parser, token):
    """
    Gets all portfolio categories.
 
    Syntax::
 
        {% get_portfolio_categories as [var_name] %}
 
    Example usage::
 
        {% get_portfolio_categories as category_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return PortfolioCategories(var_name)
    

class PortfolioProjects(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name
 
    def render(self, context):
        categories = Project.objects.all()
        context[self.var_name] = categories
        return ''
 
@register.tag
def get_portfolio_projects(parser, token):
    """
    Gets all portfolio projects.
 
    Syntax::
 
        {% get_portfolio_projects as [var_name] %}
 
    Example usage::
 
        {% get_portfolio_projects as project_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return PortfolioProjects(var_name)