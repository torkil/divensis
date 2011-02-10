from django import template

from divensis.util.decorators import basictag

register = template.Library()


# TODO: Not sure if we should use this or not...
@register.inclusion_tag('mediamanager/render_gallery.html')
def render_gallery(gallery):
    images = gallery.image_set.all()
    return {'object_list': images}