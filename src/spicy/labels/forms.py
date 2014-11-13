from django import forms
from django.utils.translation import ugettext_lazy as _
from spicy.utils.models import get_custom_model_class
from . import defaults

LabelModel = get_custom_model_class(defaults.CUSTOM_LABEL_MODEL)

class LabelForm(forms.ModelForm):
    class Meta:
        model = LabelModel
        fields = 'text', 'order_lv', 'slug', 'color'


class LabelConsumerForm(forms.ModelForm):
    labels = forms.CharField(
        label=_('Labels'), required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(LabelConsumerForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['labels'].initial = ', '.join(
                [str(lb.id) for lb in self.instance.label.all()])

    def save(self, *args, **kwargs):
        instance = super(LabelConsumerForm, self).save(*args, **kwargs)
        value = self.cleaned_data['labels']
        new_value = []
        for val in value.split(','):
            if val.find('new_'):
                new_value.append(val)
            else:
                label = LabelModel()
                label.text = val.replace('new_','',1).replace('&#44;',',')
                if label.text:
                    obj, _create = LabelModel.objects.get_or_create(
                        text__iexact=label.text)
                    if _create:
                        obj.text = label.text
                        obj.save()
                    new_value.append(obj.id)
        try:
           instance.labels =  new_value if value else []
        except:
            pass
        instance.save()
        return instance
