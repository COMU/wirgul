#! -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.main', name='main_view'),
    url(r'^new/$', 'web.views.new_user', name='new_user_view'),
    url(r'^password_change/invalid_mail/$', 'web.views.password_change', name='invalid_mail_views'),
    url(r'^password_change/$', 'web.views.password_change', name='password_change_views'),
    url(r'^get_time/$', 'web.views.get_time', name='get_time_view'),
    url(r'^guest_user/$', 'web.views.guest_user', name='guest_user_view'),
    url(r'^doesnt_exist/$', 'web.views.new_user', name='doesnt_exist_view'),
    url(r'^new/new_user_confirm/$', 'web.views.new_user', name='new_user_confirm'),
    url(r'^new/(?P<url_id>\w+)/$', 'web.views.new_user_registration', name='new_user_registration_view'),
    url(r'^get_departments/$', 'web.views.get_departments', name='get_departments'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^password_change/(?P<url_id>\w+)/$', 'web.views.password_change_registration', name='password_change_registration'),
    #url(r'^new/$', 'web.views.faculty', name='faculty'),
    #url(r'^new/$', 'web.views.faculty', name='faculty'),
    # url(r'^$', 'wirgul.views.home', name='home'),
    # url(r'^wirgul/', include('wirgul.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
