from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import defaults 

class Label(models.Model):
    consumers = models.ManyToManyField(defaults.LABELS_CONSUMER)
    text = models.CharField(_('Label text'), max_length=255, db_index=True)
    url = models.CharField(_('External url'), max_length=255)
    order_lv = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'lb_label'
        ordering = 'order_lv', 'text'

    def __unicode__(self):
        return self.text
