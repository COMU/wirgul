#! -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^captcha/', include('captcha.urls')),
    (r'^/', include('wirgul.web.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
