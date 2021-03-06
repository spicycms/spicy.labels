from django.conf.urls import patterns, include, url
from django.conf import settings


public_urls = patterns(
    'spicy.labels.views',
    url(r'^label/(?P<slug>.+)/$', 'label', name='label'),
)


admin_urls = patterns(
    'spicy.labels.admin',
    url(r'^$', 'labels_list', name='index'),
    url(r'^create/$', 'create', name='create'),
    url(r'^(?P<label_id>\d+)/$', 'edit', name='edit'),
    url(r'^delete/(?P<label_id>\d+)/$', 'delete', name='delete'),
    url(r'^autocomplete/$', 'autocomplete', name='autocomplete'),
    url(r'^data/$', 'get_data', name='get-data'),
)

if 'spicy.seo' in settings.INSTALLED_APPS:
    admin_urls += patterns(
        'spicy.labels.admin',
        url(r'^(?P<label_id>\d+)/seo/$', 'edit_label_seo', name='edit-label-seo'),
    )

urlpatterns = patterns(
    '',
    url(r'^admin/labels/', include(admin_urls, namespace='admin')),
    url(r'^', include(public_urls, namespace='public')),
)
