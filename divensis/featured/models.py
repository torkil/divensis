import datetime

from django.db import models

from divensis.mediamanager.models import ImageGallery
from django.utils.translation import ugettext_lazy as _

class FeaturedItem(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    link_text = models.CharField(max_length=100)
    gallery = models.ForeignKey(ImageGallery, verbose_name=_('gallery'))
    published_date = models.DateTimeField(_('published date'),
                                          blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _('featured item')
        verbose_name_plural = _('featured items')
        ordering = ['-published_date']
        get_latest_by = 'published_date'

    def save(self):
        if self.published_date is None:
            self.published_date = datetime.datetime.now()
        super(FeaturedItem, self).save()
