from django.contrib import admin

from markitup.widgets import AdminMarkItUpWidget

from divensis.tagsuggest.widgets import TaggingSuggestWidget
from divensis.portfolio.models import Project, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'all_categories', 'visits']
    search_fields = ['name', 'type', 'title', 'body']
    prepopulated_fields = {'slug': ['name']}
    raw_id_fields = ['gallery']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = AdminMarkItUpWidget()
        if db_field.name == 'tags':
            kwargs['widget'] = TaggingSuggestWidget()
        return super(ProjectAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
