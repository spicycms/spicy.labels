from django import forms
from django.utils.translation import ugettext_lazy as _

from spicy.labels import models


class LabelForm(forms.ModelForm):
    class Meta:
        model = models.Label
        fields = 'text', 'order_lv', 'slug'


class LabelConsumerForm(forms.ModelForm):
    labels = forms.CharField(
        label=_('Labels'), required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(LabelConsumerForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['labels'].initial = ', '.join(
                [str(lb.id) for lb in self.instance.label_set.all()])

    def save(self, *args, **kwargs):
        instance = super(LabelConsumerForm, self).save(*args, **kwargs)
        print instance
        print instance.labels
        print self.cleaned_data['labels'].split(',')
        instance.labels = self.cleaned_data['labels'].split(',')
        instance.save()
        return instance
