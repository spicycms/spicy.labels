from django.conf.urls.defaults import *


admin_urls = patterns(
     'labels.admin',

#     # labels
#     url(r'^$', 'labels', name='index'),
#     url(r'^add/$', 'label_add', name='add'),
#     url(r'^(?P<label_id>\d+)/$', 'label_edit', name='edit'),
#     url(r'^delete/$', 'label_delete', name='delete'),
)


urlpatterns = patterns(
    '',
    url(r'^admin/labels/', include(admin_urls, namespace='admin')),
    )
