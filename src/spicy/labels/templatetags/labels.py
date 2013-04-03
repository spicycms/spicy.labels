from __future__ import absolute_import
import datetime
from blog import defaults as bl_defaults
from django import template
from django.db.models import Count
from labels import models

register = template.Library()


@register.filter
def top_labels(num):
    now = datetime.datetime.now()
    return models.Label.objects.filter(
        document__is_public=True, document__pub_date__lte=now,
        document__state=bl_defaults.STATE_APPROVED
        ).values('text').annotate(
        Count('text')).order_by('-text__count')[:num]
