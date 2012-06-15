from django.conf.urls import patterns, url,include
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.main', name='main_view'),
    url(r'^new/$', 'web.views.new_user', name='new_user_view'),
    url(r'^captcha/', include('captcha.urls')),
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