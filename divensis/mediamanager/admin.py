from django.contrib import admin

from divensis.mediamanager.models import Image, ImageGallery

class ImageInline(admin.TabularInline):
    max_num = 10
    model = Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_filename', 'title', 'gallery', 'admin_thumbnail_view']
    search_fields = ['image', 'title']

class ImageGalleryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']
    inlines = [
        ImageInline,
    ]

admin.site.register(Image, ImageAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)
