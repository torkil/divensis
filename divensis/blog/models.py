import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from tagging.fields import TagField
from django_markup.fields import MarkupField
from django_markup.markup import formatter

from divensis.blog.managers import PublicManager
from divensis.mediamanager.models import ImageGallery

class Category(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['title']

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('blog_category_detail', None, {'slug': self.slug})


class Post(models.Model):
    # Constants for status choices
    STATUS_DRAFT, STATUS_PUBLIC = 1, 2

    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PUBLIC, _('Public'))
    )

    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    author = models.ForeignKey(User, editable=False, blank=True, null=True)

    gallery = models.ForeignKey(ImageGallery, blank=True, null=True, verbose_name=_('gallery'))

    created_date = models.DateTimeField(_('created date'), auto_now_add=True)
    modified_date = models.DateTimeField(_('edited date'), auto_now=True)
    published_date = models.DateTimeField(_('published date'),
                                          blank=True)

    markup = MarkupField(default='markdown')
    body = models.TextField(_('body'))
    body_html = models.TextField(editable=False, blank=True)

    excerpt = models.TextField(_('excerpt'), blank=True)

    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_PUBLIC)
    categories = models.ManyToManyField(Category)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    visits = models.IntegerField(_('visits'), default=0, editable=False)
    tags = TagField()

    objects = PublicManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-published_date']
        get_latest_by = 'published_date'

    def __unicode__(self):
        return u'%s' % self.title

    def all_categories(self):
        categories = []
        for category in self.categories.all():
            categories.append(category.title)
        return ", ".join(categories)
    all_categories.short_description = _('Categories')

    def is_public(self):
        return self.status == self.STATUS_PUBLIC
    is_public.short_description = _('Public')
    is_public.boolean = True
    is_public.admin_order_field = 'status'
    
    def save(self):
        if self.published_date is None:
            self.published_date = datetime.datetime.now()
        self.body_html = formatter(self.body, filter_name=self.markup)
        super(Post, self).save()

    @permalink
    def get_absolute_url(self):
        return ('blog_detail', None, {
            'year': self.published_date.year,
            'month': self.published_date.strftime('%m').lower(),
            'day': self.published_date.day,
            'slug': self.slug
        })

    def get_previous_post(self):
        return self.get_previous_by_published_date(status__gte=self.STATUS_PUBLIC)

    def get_next_post(self):
        return self.get_next_by_published_date(status__gte=self.STATUS_PUBLIC)
