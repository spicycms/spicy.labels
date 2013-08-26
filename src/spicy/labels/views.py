# _*_ coding: utf-8 _*_
from spicy.core.siteskin.decorators import render_to
from spicy.labels import models


@render_to('spicy.labels/label.html', use_siteskin=True)
def label(request, lab_id):
    doc = models.Label.objects.get(pk=lab_id)
    return {'doc': doc}
