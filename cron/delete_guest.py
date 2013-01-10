#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import os
import datetime
from django.conf import settings


print "running:", datetime.datetime.now().isoformat()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wirgul.settings'

from wirgul.web.models import *
from wirgul.utils.ldapmanager import *

ldap_manager = LdapHandler()
ldap_manager.connect()
ldap_manager.bind()

active_guests = GuestUser.objects.filter(status=True)

for guest in active_guests:

    now = datetime.datetime.now()

    if now >= guest.deadline_time:
        print "found:", guest.guest_user_email
        prefix = guest. guest_user_email.split("@")[0]
        guest_user_email = "@".join([prefix, settings.EDUROAM_DOMAIN])
        if ldap_manager.search(guest_user_email) > 0:
            try:
                ldap_manager.del_user(guest_user_email)
                print "Deadline: %s Application: %s Deleted: %s " % (str(guest.deadline_time.isoformat()), str(guest.application_time.isoformat()), guest_user_email)
                guest.status = False
                guest.save()
            except Exception, ex:
                print ex

ldap_manager.unbind()