from django.conf.urls.defaults import *


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
    )
