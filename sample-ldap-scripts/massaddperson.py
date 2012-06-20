#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import os
import sendhtmlmail

sys.path.append("/home/oguz/workspace/")
#print sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'ldaplogin.settings'


from ldaplogin.users.models import *
from ldapmanager import *
import ldap.modlist as modlist
import datetime
import time

count = 0
pre = 0
post = 0
max_status = False
if len(sys.argv) > 1:
    pre = sys.argv[1]
    post = sys.argv[2]
    print pre, post
    #sys.exit(-1)
else:
    max_status = True

op = Operations()

try:
    op.connect()
    op.bind()
except Exception, ex:
    print ex
    sys.exit(-1)

if max_status:
    people = Person.objects.filter(eduroam_will_status=True)
else:
    people = Person.objects.filter(eduroam_will_status=True)[pre:post]

attrs = dict()
attributes = []
f = file("time.txt", "w")
counter = 0
for person in people:
    if op.search(person.email, member_type="personel"):
        print "User already added:", person.email
        print "Deleting the user:"
        op.del_user(person.email, member_type="personel")

    mail_str="mail="+person.email
    dn = ",".join([mail_str,"ou=personel","ou=people","dc=comu","dc=edu","dc=tr"])
    objectclass = ['organizationalPerson','radiusprofile','person','inetOrgPerson']
    if person.middle_name:
        middle_name = person.middle_name
    else:
        middle_name = ""
    cn = " ".join([person.first_name,middle_name,person.surname])
    givenname = person.first_name
    email = person.email
    sn= person.surname
    uid = person.email
    userpassword = person.secret.password
    attrs['cn'] = [cn.encode("utf-8")]
    attrs['givenName'] = [givenname.encode("utf-8")]
    attrs['mail'] = [email.encode("utf-8")]
    attrs['objectClass'] = objectclass
    attrs['sn'] = [sn.encode("utf-8")]
    attrs['uid'] = [uid.encode("utf-8")]
    attrs['userPassword'] = [userpassword.encode("utf-8")]
    ldif = modlist.addModlist(attrs)
    try:
        op.add_formatted(dn, ldif)
	dt = datetime.datetime.now()
	print "Time:", dt.isoformat()
        print "Adding:", person.email, userpassword
        print "Sending mail:", person.email
	s = " ".join([dt.isoformat(), person.email, userpassword, "\n"])
	f.write(s)
	print cn, email, userpassword, email
        sendhtmlmail.mailsend(cn, email, userpassword, email)
	counter += 1
	time.sleep(5)
    except Exception, ex:
        print ex
        sys.exit(-1)

print "\n"
print "Number of the sent mails:", counter
print "Number of people:", len(people)

f.close()
