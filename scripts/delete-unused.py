import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'wirgul.settings'


from wirgul.web.models import GuestUser
from wirgul.utils.ldapmanager import LdapHandler

ldap_handler = LdapHandler()

if ldap_handler.connect():
    ldap_handler.bind()
else:
    print "Error in connecting Ldap"
    sys.exit(-1)

guests = GuestUser.objects.filter(status=True)

for guest in guests:

    now = datetime.datetime.now()
    if now > guest.deadline_time:
        email = "@".join([guest.citizen_no, "comu.edu.tr"])
        user = ldap_handler.search(email)
        if user == 1:
            print "deleting", email
            ldap_handler.del_user(email)
            guest.status = False
            guest.save()
        if user > 1:
            print "Error: more than one user is added to the ldap"

ldap_handler.unbind()