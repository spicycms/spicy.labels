# _*_ coding: utf-8 _*_
from spicy.core.siteskin.decorators import render_to
from spicy.labels import models
from django.shortcuts import get_object_or_404


@render_to('spicy.labels/label.html', use_siteskin=True)
def label(request, slug):
    slug = slug.split('+')
    docs = []
    for s in slug:
        obj = get_object_or_404(models.Label, slug=s)
        docs.append(obj)
    return {'docs': docs}

