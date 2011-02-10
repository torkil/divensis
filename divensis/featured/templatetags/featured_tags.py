from django import template

from divensis.featured.models import FeaturedItem

register = template.Library()


@register.inclusion_tag('featured/featured_item.html')
def render_featured_item():
    try:
        featured = FeaturedItem.objects.all()[:1].get()
        return {'object': featured}
    except:
        pass
