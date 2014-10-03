from django.db import models
from django.utils.translation import ugettext_lazy as _
import re
from . import defaults

from spicy.labels import widget


class Label(models.Model):
    consumers = models.ManyToManyField(defaults.LABELS_CONSUMER)
    text = models.CharField(_('Label text'), max_length=255, db_index=True)
    slug = widget.RuSlugField(_('Slug'), blank=False, max_length=100)
    url = models.CharField(_('External url'), max_length=255)
    order_lv = models.PositiveSmallIntegerField(_('Position'), default=0)
    color = models.CharField(
        choices=defaults.LABEL_CHOICE_COLOR, verbose_name=_('Color or Class'),
        max_length=100, default=defaults.LABEL_CHOICE_COLOR_DEFAULT)

    class Meta:
        db_table = 'lb_label'
        ordering = 'order_lv', 'text'

    def __unicode__(self):
        return self.text

    def get_slugs(self):
        all_labels = Label.objects.values('slug')
        labels = [label['slug'] for label in all_labels]
        return labels

    def save(self, *args, **kwargs):
        text = re.compile(u'(\W+)', re.UNICODE)
        label = text.sub(' ', self.text)
        self.slug = label.lower().strip().replace(' ', '-')
        print self.slug, self.get_slugs()
        if self.slug not in self.get_slugs():
            super(Label, self).save()

    @models.permalink
    def get_absolute_url(self):
        return 'labels:public:label', None, {'slug': self.slug}
