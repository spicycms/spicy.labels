from . import models
from django import forms

class LabelForm(forms.ModelForm):
    class Meta:
        model = models.Label
        fields = 'text', 'order_lv'
