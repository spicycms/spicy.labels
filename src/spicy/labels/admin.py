# coding=utf-8
from django import http
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from spicy.core.admin import defaults as admin_defaults
from spicy.core.admin.conf import AdminAppBase, AdminLink
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import ajax_request, render_to
from spicy.utils import NavigationFilter
from spicy.utils.models import get_custom_model_class
from . import defaults, forms

LabelModel = get_custom_model_class(defaults.CUSTOM_LABEL_MODEL)


class AdminApp(AdminAppBase):
    name = 'labels'
    label = _('Labels')
    order_number = 3

    menu_items = (
        AdminLink(
            'labels:admin:create', _('Create label'),
            icon_class='icon-tag', perms='labels.add_label'),
        AdminLink(
            'labels:admin:index', _('All labels'), icon_class='icon-cog',
            perms='labels.change_label'
        ),
    )

    dashboard_links = [
        AdminLink(
            'labels:admin:create', _('Create label'),
            LabelModel.objects.count(), icon_class='icon-tag',
            perms='perms.add_label'
        )
    ]

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
        LabelModel, obj_per_page=admin_defaults.ADMIN_OBJECTS_PER_PAGE)
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
    label = get_object_or_404(LabelModel, pk=label_id)
    if request.method == 'POST':
        form = forms.LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
#            return http.HttpResponseRedirect(reverse(
#                'labels:admin:index'))
    else:
        form = forms.LabelForm(instance=label)
    return {'form': form, 'instance': label, 'tab': 'label'}


@is_staff(required_perms='labels.delete_label')
@render_to('delete.html', use_admin=True)
def delete(request, label_id):
    message = ''
    status = 'ok'

    label = get_object_or_404(LabelModel, pk=label_id)

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
        for label in LabelModel.objects.filter(
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
    labels = LabelModel.objects.filter(**search_kwargs)
    return [{'title': label.text, 'id': label.pk} for label in labels]


@ajax_request
def get_data(request):
    g_ids = []
    for val in request.GET['ids'].split(','):
        if val.find('new_'):
            g_ids.append(val)
    ids = [int(id) for id in g_ids]
    objects = list(LabelModel.objects.filter(pk__in=ids))
    objects.sort(key=lambda obj: ids.index(obj.pk))
    return [{'id': obj.pk, 'text': obj.text} for obj in objects]


@is_staff(required_perms='seo.change_seo_content')
@render_to('edit_seo.html', use_admin=True)
def edit_label_seo(request, label_id):
    page = get_object_or_404(LabelModel, pk=label_id)
    class_name = page.__class__.__name__
    return {'instance': page, 'tab': 'seo', 'class_name': class_name}
