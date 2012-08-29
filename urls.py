#! -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'wirgul.web.views.main', name='main_view'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^captcha/', include('captcha.urls')),
    (r'^user/', include('wirgul.web.urls')),
)

if settings.DEVELOPMENT_SERVER:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
