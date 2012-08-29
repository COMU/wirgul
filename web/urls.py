from django.conf.urls.defaults import *
from wirgul.web.views import *

urlpatterns = patterns('',
    url(r'^new/$', view=new_user, name='new_user_view'),
    url(r'^new/(?P<url_id>\w+)/$', view=new_user_registration, name='new_user_registration_view'),
    url(r'^new_password/$', view=new_password, name='new_password_view'),
    url(r'^new_password/(?P<url_id>\w+)/$', view=new_password_registration, name='new_password_registration'),
    url(r'^guest_user/$', view=guest_user, name='guest_user_view'),
    url(r'^guest_user/(?P<url_id>\w+)/$', view=guest_user_registration, name='guest_user_registration_view'),
    #url(r'^already_exist/$', view=new_user, name='new_user_already_exist_view'),
    #url(r'^password_change/invalid_mail/$', view=password_change, name='invalid_mail_view'),
    url(r'^get_times/$', view=get_times, name='get_times'),
    url(r'^guest_user/$', view=guest_user, name='guest_user_view'),
    #url(r'^doesnt_exist/$', view=new_user, name='doesnt_exist_view'),
    #url(r'^new/new_user_confirm/$', view=new_user, name='new_user_confirm'),
    url(r'^get_departments/$', view=get_departments, name='get_departments'),

    )