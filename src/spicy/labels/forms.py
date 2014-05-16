from django import forms
from django.utils.translation import ugettext_lazy as _
from spicy.labels import models


class LabelForm(forms.ModelForm):
    class Meta:
        model = models.Label
        fields = 'text', 'order_lv', 'slug', 'color'


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
        value = self.cleaned_data['labels']
        new_value = []
        for val in value.split(','):
            if val.find('new_'):
                new_value.append(val)
            else:
                label = models.Label()
                label.text = val.replace('new_','',1)
                if label.text:
                    label.save()
                    new_value.append(label.id)
        instance.labels =  new_value if value else []
        instance.save()
        return instance
