import datetime
from haystack import indexes
from haystack import site
from divensis.blog.models import Post, Category

class PostIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField()
    
    # published date
    pub_date = indexes.DateTimeField(model_attr='published_date')
    is_public = indexes.BooleanField()
    
    # tumbleweed fields
    title = indexes.CharField(model_attr='title', indexed=False)
    url = indexes.CharField(indexed=False)
    image = indexes.CharField(model_attr='gallery', null=True,indexed=False)
    excerpt = indexes.CharField(model_attr='excerpt', indexed=False)
    body_html = indexes.CharField(model_attr='body_html', indexed=False)
    categories = indexes.MultiValueField(indexed=False, null=True)
    
    def prepare_categories(self, obj):
        return [{'title':category.title, 'url':category.get_absolute_url()} for category in obj.categories.all()]
    
    def prepare_is_public(self, obj):
        return obj.is_public()
    
    def prepare_author(self, obj):
        full_name = obj.author.get_full_name()
        if full_name == '':
            return obj.author.username
        return full_name
    
    def prepare_url(self, obj):
        return obj.get_absolute_url()

    def prepare_image(self, obj):
        if obj.gallery is not None:
            return obj.gallery.image_set.all()[:1].get().blog_list.url
        return ""
    
    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Post.objects.all()

site.register(Post, PostIndex)
