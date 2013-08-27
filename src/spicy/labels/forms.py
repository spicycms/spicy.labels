from django import forms
from django.utils.translation import ugettext_lazy as _

from spicy.labels import models


class LabelForm(forms.ModelForm):
    class Meta:
        model = models.Label
        fields = 'text', 'order_lv', 'slug'


class LabelConsumerForm(forms.ModelForm):
    labels = forms.CharField(label=_('Labels'), required=False)

    def __init__(self, *args, **kwargs):
        super(LabelConsumerForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['labels'].initial = ', '.join(
                [lb.text for lb in self.instance.label_set.all()])

    def save(self, *args, **kwargs):
        instance = super(LabelConsumerForm, self).save(*args, **kwargs)

        labels = self.cleaned_data['labels'].split(',')

        if labels and self.instance.pk:
            exists_labels = list(models.Label.objects.filter(text__in=labels))

            #create new labels
            for label in (set(labels) - set([lb.text for lb in exists_labels])):
                label, created = models.Label.objects.get_or_create(text=label)
                exists_labels.append(label)

            instance.label_set.clear()
            instance.label_set.add(*exists_labels)

        return instance
