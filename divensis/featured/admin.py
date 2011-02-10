from django.contrib import admin

from divensis.featured.models import FeaturedItem

class FeaturedItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'gallery', 'url']
    list_filter = ['title']
    search_fields = ['title']
    raw_id_fields = ['gallery']


admin.site.register(FeaturedItem, FeaturedItemAdmin)
