from django.db import models
from django.utils.translation import ugettext_lazy as _
from presscenter import utils

DocumentModel = utils.get_concrete_document()

class Label(models.Model):
    document = models.ForeignKey(DocumentModel)
    text = models.CharField(_('Label text'), max_length=255, db_index=True)
    order_lv = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'lb_label'
        unique_together = ('document', 'text'),
        ordering = 'order_lv', 'text'

    def __unicode__(self):
        return self.text
