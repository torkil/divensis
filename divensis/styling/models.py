from django.db import models
from django.utils.translation import ugettext_lazy as _


class Stylesheet(models.Model):
    url = models.CharField(_('Relative URL'), max_length=200)
    css = models.TextField(_('CSS'))
    modified_date = models.DateTimeField(_('edited date'), auto_now=True)

    class Meta:
        verbose_name = _('stylesheet')
        verbose_name_plural = _('stylesheets')

    def __unicode__(self):
        return u'Stylesheet for URL: %s' % self.url
