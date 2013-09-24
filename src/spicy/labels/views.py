# _*_ coding: utf-8 _*_
from spicy.core.siteskin.decorators import render_to
from spicy.labels import models
from django.shortcuts import get_object_or_404
from spicy.presscenter import defaults
from spicy.utils.models import get_custom_model_class

Document = get_custom_model_class(defaults.CUSTOM_DOCUMENT_MODEL)

@render_to('spicy.labels/label.html', use_siteskin=True)
def label(request, slug):
    slug = slug.split('+')
    labels = []
    for s in slug:
        obj = get_object_or_404(models.Label, slug=s)
        labels.append(obj)
    try:
        docs = Document.pub_objects.filter(label__in=labels)
    except AttributeError:
        docs = Document.objects.filter(label__in=labels)
    return {'docs': docs, 'labels': labels}
