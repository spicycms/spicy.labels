# coding=utf-8
from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from spicy.core.admin import defaults as admin_defaults
from spicy.core.admin.conf import AdminAppBase, AdminLink, Perms
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import ajax_request, render_to
from spicy.utils import NavigationFilter
from . import forms, models


class AdminApp(AdminAppBase):
    name = 'labels'
    label = _('Labels')
    order_number = 3

    menu_items = (
        AdminLink('labels:admin:create', _('Create label')),
        AdminLink('labels:admin:index', _('All labels')),
    )

    create = AdminLink('labels:admin:create', _('Create label'),)

    perms = Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff(required_perms='labels.change_label')
@render_to('list.html', use_admin=True)
def labels_list(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(
        models.Label, obj_per_page=admin_defaults.ADMIN_OBJECTS_PER_PAGE)
    objects_list = paginator.current_page.object_list
    return {'paginator': paginator, 'objects_list': objects_list, 'nav': nav}


@is_staff(required_perms='labels.add_label')
@render_to('create.html', use_admin=True)
def create(request):
    if request.method == 'POST':
        form = forms.LabelForm(request.POST)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse(
                'labels:admin:index'))
    else:
        form = forms.LabelForm()
    return {'form': form}


@is_staff(required_perms='labels.change_label')
@render_to('edit.html', use_admin=True)
def edit(request, label_id):
    label = get_object_or_404(models.Label, pk=label_id)
    if request.method == 'POST':
        form = forms.LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse(
                'labels:admin:index'))
    else:
        form = forms.LabelForm(instance=label)
    return {'form': form, 'instance': label}


@is_staff(required_perms='labels.delete_label')
@render_to('delete.html', use_admin=True)
def delete(request, label_id):
    message = ''
    status = 'ok'

    label = get_object_or_404(models.Label, pk=label_id)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            label.delete()
            return http.HttpResponseRedirect(
                reverse('labels:admin:index'))

    return dict(message=unicode(message), status=status, instance=label)


@is_staff(required_perms='labels.delete_label')
@ajax_request
def delete_from_list(request):
    message = ''
    status = 'ok'
    try:
        for label in models.Label.objects.filter(
                id__in=request.POST.getlist('id')):
            label.delete()
        message = _('All objects have been deleted successfully')
    except KeyError, e:
        message = unicode(e)
        status = 'error'
    except Exception, e:
        print e
    return dict(message=unicode(message), status=status)


@ajax_request
def autocomplete(request):
    search_kwargs = dict(text__icontains=request.GET.get('search', ''))
    labels = models.Label.objects.filter(**search_kwargs)
    return [{'title': label.text, 'id': label.pk} for label in labels]


@ajax_request
def get_data(request):
    g_ids = []
    for val in request.GET['ids'].split(','):
        if val.find('new_'):
            g_ids.append(val)
    ids = [int(id) for id in g_ids]
    objects = list(models.Label.objects.filter(pk__in=ids))
    objects.sort(key=lambda obj: ids.index(obj.pk))
    return [{'id': obj.pk, 'text': obj.text} for obj in objects]
