import datetime
from haystack import indexes
from haystack import site
from divensis.portfolio.models import Project

class ProjectIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    
    # published date
    pub_date = indexes.DateTimeField(model_attr='published_date')
    is_public = indexes.BooleanField()
    
    # tumbleweed fields
    title = indexes.CharField(model_attr='front_title', indexed=False)
    url = indexes.CharField(indexed=False)
    image = indexes.CharField(model_attr='gallery', null=True, indexed=False)
    excerpt = indexes.CharField(model_attr='front_excerpt', indexed=False)
    body_html = indexes.CharField(model_attr='body_html', indexed=False)
    
    def prepare_is_public(self, obj):
        return True
    
    def prepare_url(self, obj):
        return obj.get_absolute_url()

    def prepare_image(self, obj):
        if obj.gallery is not None:
            return obj.gallery.image_set.all()[:1].get().blog_list.url
        return ""

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Project.objects.all()

site.register(Project, ProjectIndex)
