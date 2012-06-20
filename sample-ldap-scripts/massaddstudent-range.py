#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import os
import time

sys.path.append("/home/oguz/workspace/")
#print sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'ldaplogin.settings'


from ldaplogin.users.models import *
from ldapmanager import *
import ldap.modlist as modlist

for i in range(31394,31395):

    count = 0
    filter_status = True
    max_status = False

    # use thsi for mass add for all students
    #pre = 10 * i
    #post = 10 * i + 10
    pre = i
    post = i+1

    op = Operations()

    try:
        op.connect()
        op.bind()
    except Exception, ex:
        print ex
        sys.exit(-1)

    if max_status:
        students = Student.objects.all()
    elif filter_status:
        students = Student.objects.all()[pre:post]
        print "\n\n", pre, post
    else:
        students = Student.objects.filter(email=student_email)
    attrs = dict()
    attributes = []
    for student in students:
        student.ldap_status = False
        if student.ldap_status:
            print student.email, " already added"
            continue
        print op.search(student.email, member_type="ogrenci")
        if op.search(student.email, member_type="ogrenci"):
            print "User already added:", student.email
            print "Deleting the user:", student.email
            op.del_user(student.email, member_type="ogrenci")

        mail_str="mail="+student.email
        dn = ",".join([mail_str,"ou=ogrenci","ou=people","dc=comu","dc=edu","dc=tr"])
        objectclass = ['organizationalPerson','radiusprofile','person','inetOrgPerson']
        if student.middle_name:
            middle_name = student.middle_name
        else:
            middle_name = ""
        cn = " ".join([student.first_name,middle_name,student.surname])
        givenname = student.first_name
        email = student.email
        sn= student.surname
        uid = student.email
        userpassword = student.student_secret.password
        attrs['cn'] = [cn.encode("utf-8")]
        attrs['givenName'] = [givenname.encode("utf-8")]
        attrs['mail'] = [email.encode("utf-8")]
        attrs['objectClass'] = objectclass
        attrs['sn'] = [sn.encode("utf-8")]
        attrs['uid'] = [uid.encode("utf-8")]
        attrs['userPassword'] = [userpassword.encode("utf-8")]
        ldif = modlist.addModlist(attrs)
        #print dn, ldif
        try:
            op.add_formatted(dn, ldif)
            print "Adding:", student.email
            student.ldap_status = True
            student.save()
        except Exception, ex:
            print ex
            sys.exit(-1)
        #time.sleep(2)
    op.unbind()
    time.sleep(5)
