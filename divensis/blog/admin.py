import datetime

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext_lazy as _n

from markitup.widgets import AdminMarkItUpWidget

from divensis.blog.models import Post, Category
from divensis.tagsuggest.widgets import TaggingSuggestWidget

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'all_categories', 'published_date', 'is_public', 'visits']
    list_filter = ['published_date', 'categories', 'status']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_published', 'make_withdrawn']
    raw_id_fields = ['gallery']
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = AdminMarkItUpWidget()
        if db_field.name == 'tags':
            kwargs['widget'] = TaggingSuggestWidget()
        return super(PostAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    
    # Dropdown action to publish selected entries
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status=Post.STATUS_PUBLIC)
        
        # Set published_date on entries that doesn't have one
        # workaround for http://code.djangoproject.com/ticket/12142
        if queryset.filter(published_date__isnull=True).count() > 0:
            queryset.filter(published_date__isnull=True).update(
                published_date=datetime.datetime.now()
            )
        message = _n('%(num)d post was published.',
                     '%(num)d posts were published.',
                     rows_updated) % {'num': rows_updated,}
        self.message_user(request, message)
    make_published.short_description = _('Publish selected')
    
    # Dropdown action to withdraw selected entries
    def make_withdrawn(self, request, queryset):
        rows_updated = queryset.update(status=Post.STATUS_DRAFT)
        message = _n('%(num)d post was withdrawn.',
                                 '%(num)d posts were withdrawn.',
                                 rows_updated) % {'num': rows_updated,}
        self.message_user(request, message)
    make_withdrawn.short_description = _('Withdraw marked')
    
    def save_model(self, request, obj, form, change):
        if not change:
            # Automatically populate author field if it's a new entry
            obj.author = request.user
        obj.save()

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
