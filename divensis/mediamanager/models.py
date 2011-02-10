from django.db import models
from django.utils.translation import ugettext_lazy as _

#import imagekit
from imagekit.models import ImageModel, CROP_HORZ_CHOICES, CROP_VERT_CHOICES


class ImageGallery(models.Model):
    title  = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    #images = models.ManyToManyField()

    class Meta:
        verbose_name = _('image gallery')
        verbose_name_plural = _('image galleries')
        ordering = ['title']

    def get_first_image(self):
        return self.image_set.all()[:1].get()

    def __unicode__(self):
        return u'%s' % self.title


class Image(ImageModel):
    title = models.CharField(_('title'), max_length=100, blank=True)
    image = models.ImageField(_('image'), upload_to='uploads/images')
    caption = models.CharField(_('caption'), max_length=150, blank=True)
    order = models.PositiveIntegerField(_('order'), blank=True, null=True)
    gallery = models.ForeignKey(ImageGallery, verbose_name=_('gallery'))

    crop_horz = models.SmallIntegerField(_('horizontal crop'),
                                         choices=CROP_HORZ_CHOICES,
                                         default=CROP_HORZ_CHOICES[1][0])
    crop_vert = models.SmallIntegerField(_('vertical crop'),
                                         choices=CROP_VERT_CHOICES,
                                         default=CROP_VERT_CHOICES[1][0])

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ['order']

    class IKOptions:
        spec_module = 'divensis.mediamanager.specs'
        cache_dir = 'uploads/images/cache'
        crop_horz_field = 'crop_horz'
        crop_vert_field = 'crop_vert'
        admin_thumbnail_spec = 'admin_thumbnail'
        image_field = 'image'
        save_count_as = None

    def __unicode__(self):
        return u'%s' % self.title

    def image_filename(self):
        return self.image.__unicode__().split('uploads/images')[1]
    image_filename.short_description = _('Image')
    image_filename.admin_order_field = 'image'
