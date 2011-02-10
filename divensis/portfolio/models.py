import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import permalink

from tagging.fields import TagField
from django_markup.fields import MarkupField
from django_markup.markup import formatter

from divensis.mediamanager.models import ImageGallery


class Category(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    order = models.PositiveIntegerField(_('order'), blank=True, null=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('order',)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('portfolio_category_detail', None, {
            'slug': self.slug
        })


class Project(models.Model):
    name = models.CharField(_('project name'), max_length=100)
    type = models.CharField(_('project type'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    published_date = models.DateTimeField(_('published date'), blank=True)
    gallery = models.ForeignKey(ImageGallery, blank=True, null=True, verbose_name=_('gallery'))

    title = models.CharField(_('title'), max_length=100, blank=False)
    markup = MarkupField(default='markdown')
    body = models.TextField(_('body'))
    body_html = models.TextField(editable=False, blank=True)

    details = models.TextField(_('project details'), blank=True)

    front_title = models.CharField(_('front page title'), max_length=100, blank=True)
    front_excerpt = models.TextField(_('front page excerpt'), blank=True)

    categories = models.ManyToManyField(Category, blank=True)

    visits = models.IntegerField(_('visits'), default=0, editable=False)
    tags = TagField()
    
    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ['-published_date']

    def __unicode__(self):
        return u'%s' % self.title

    def all_categories(self):
        categories = []
        for category in self.categories.all():
            categories.append(category.title)
        return u', '.join(categories)
    all_categories.short_description = _('Categories')
    
    def all_categories_slugified(self):
        categories = []
        for category in self.categories.all():
            categories.append(category.slug)
        # separate by spaces
        return u' '.join(categories)
    
    def save(self):
        if self.front_title.strip() == "":
            self.front_title = self.title
        if self.published_date is None:
            self.published_date = datetime.datetime.now()
        self.body_html = formatter(self.body, filter_name=self.markup)
        super(Project, self).save()

    @permalink
    def get_absolute_url(self):
        return ('portfolio_detail', None, {
            'slug': self.slug
        })
