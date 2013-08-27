from django.conf.urls import patterns, include, url


public_urls = patterns(
    'spicy.labels.views',
#    url(r'^label/(?P<lab_id>\d+)/$', 'label', name='label'),
    url(r'^label/(?P<slug>.+)/$', 'label', name='label'),
)
admin_urls = patterns(
     'spicy.labels.admin',

     # labels
     url(r'^$', 'labels_list', name='index'),
     url(r'^create/$', 'create', name='create'),
     url(r'^(?P<label_id>\d+)/$', 'edit', name='edit'),
     url(r'^delete/$', 'delete', name='delete'),
)


urlpatterns = patterns(
    '',
    url(r'^admin/labels/', include(admin_urls, namespace='admin')),
    url(r'^', include(public_urls, namespace='public'))
    )
