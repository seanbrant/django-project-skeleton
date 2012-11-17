from os.path import join

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(
        r'^{0}$'.format(join(settings.STATIC_URL, r'(?P<path>.*)')[1:]),
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT},
    ),
)
