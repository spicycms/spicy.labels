from django import template
from django.db.models import Count
from spicy.labels import models
import datetime

register = template.Library()


@register.filter
def top_labels(num):
    now = datetime.datetime.now()
    return models.Label.objects.filter(
            document__is_public=True, document__pub_date__lte=now,
        ).values('text').annotate(Count('text')).order_by('-text__count')[:num]


@register.simple_tag(takes_context=True)
def all_labels(context, num=None):
    context['labels'] = models.Label.objects.annotate(
        Count('consumers')).select_related().order_by('-consumers__count')[:num]
    return "" 
