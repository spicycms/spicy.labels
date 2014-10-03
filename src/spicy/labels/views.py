# _*_ coding: utf-8 _*_
from spicy.core.siteskin.decorators import render_to
from spicy.labels import models
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage
from spicy.presscenter import defaults
from spicy.utils.models import get_custom_model_class
from django import http

Document = get_custom_model_class(defaults.CUSTOM_DOCUMENT_MODEL)

@render_to('spicy.labels/label.html', use_siteskin=True)
def label(request, slug):
    slug = slug.split('+')
    labels = []
    for s in slug:
        objs = models.Label.objects.filter(slug=s)
        if objs:
            for obj in objs:
                labels.append(obj)
        else:
            raise http.Http404
    try:
        docs = Document.pub_objects.filter(label__in=labels)
    except AttributeError:
        docs = Document.objects.filter(label__in=labels)
    if request:
        try:
            page_num = int(request.GET.get('page', 1))
        except ValueError:
            page_num = 1
    paginator = Paginator(docs, defaults.DEFAULTS_DOCS_PER_PAGE)
    page = paginator.page(page_num)
    paginator.current_page = page
    docs = page.object_list
       
    return {'docs': docs, 'labels': labels, 'paginator': paginator}
