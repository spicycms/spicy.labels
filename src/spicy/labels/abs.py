import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from spicy.core.service import api
from spicy.labels import widget, defaults


class AbstractLabelsConsumer(models.Model):

    class Meta:
        abstract = True

    @property
    def labels(self):
        return self.label.all()

    @labels.setter
    def labels(self, ids):
        """
        Set labels from ids.
        """
        self.label.clear()

        for label_id in ids:
            api.register['label'].get_label(pk=label_id).consumers.add(self)


class AbstractLabel(models.Model):
    consumers = models.ManyToManyField(defaults.LABELS_CONSUMER,
                                       related_name='label')
    text = models.CharField(_('Label text'), max_length=255, db_index=True)
    slug = widget.RuSlugField(
        _('Slug'), blank=False, max_length=100, unique=True)
    url = models.CharField(_('External url'), max_length=255)
    order_lv = models.PositiveSmallIntegerField(_('Position'), default=0)
    color = models.CharField(
        choices=defaults.LABEL_CHOICE_COLOR, verbose_name=_('Color or Class'),
        max_length=100, default=defaults.LABEL_CHOICE_COLOR_DEFAULT)

    def __init__(self, *args, **kwargs):
        super(AbstractLabel, self).__init__(*args, **kwargs)
        self._prev_text = self.text

    class Meta:
        abstract = True
        db_table = 'lb_label'
        ordering = 'order_lv', 'text'

    def __unicode__(self):
        return self.text

    def title(self):
        return self.text

    def save(self, *args, **kwargs):

        text = re.compile(u'(\W+)', re.UNICODE)
        label = text.sub(' ', self.text)

        if self._prev_text != self.text:
            self.slug = label.lower().strip().replace(' ', '-')

        super(AbstractLabel, self).save()

    @models.permalink
    def get_absolute_url(self):
        return 'labels:public:label', None, {'slug': self.slug}
