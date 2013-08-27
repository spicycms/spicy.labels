#! /usr/bin/env python
# -*- coding: utf-8 -*- 

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.db import models
from django.conf import settings
import urlparse


ALLOWED_SLUG_CHARS =                                                                                                  u'1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZйцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ-'


def patch_admin_form(form):
    js_file = urlparse.urljoin(settings.MEDIA_URL, 'js/ruslug-urlify.js')
    form.Media.js = form.Media.js + (js_file,)
    return form


class RuSlugFormField(forms.CharField):
    def __init__(self, max_length=None, min_length=None, error_message=None, *args, **kwargs):
        if error_message:
            error_messages = kwargs.get('error_messages') or {}
            error_messages['invalid'] = error_message
            kwargs['error_messages'] = error_messages
        super(RuSlugFormField, self).__init__(max_length, min_length, *args, **kwargs)

    def clean(self, value):
        if value == u'':
            return value

        for letter in value:
            if letter not in ALLOWED_SLUG_CHARS:
                raise forms.ValidationError(self.error_messages['invalid'])

        return value


class RuSlugField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': RuSlugFormField,
            'error_messages': {
                'invalid': _(u"Enter a valid 'slug' consisting of letters, numbers,"
                             u" underscores or hyphens."),
            }
        }
        defaults.update(kwargs)
        return super(RuSlugField, self).formfield(**defaults)
