#! -*- coding: utf-8 -*-
import ldap
import string
from random import choice
import ldap.modlist as modlist
from web.models import FirstTimeUser
from django.core.mail import EmailMultiAlternatives

def generate_passwd():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(5)])
    return url_id

def ldap_add_new_user(request):
    l = ldap.open("127.0.0.1")
    l.protocol_version = ldap.VERSION3
    username = "cn=admin, dc=comu,dc=edu,dc=tr"
    password  = "ldap123"
    l.simple_bind_s(username, password)
    dn="mail=melike@comu.edu.tr,ou=personel,ou=people,dc=comu,dc=edu,dc=tr"
    attrs = {}
    attrs['objectclass'] = ['organizationalPerson','person','inetOrgPerson']
    f = FirstTimeUser.objects.all()
    length = f.count() - 1
    array_obj = FirstTimeUser.objects.values_list('name','surname','email')
    attrs['givenName'] = str(array_obj[length][0])
    attrs['sn'] = str(array_obj[length][1])
    attrs['cn'] = str(array_obj[length][0]) + str(array_obj[length][1])
    attrs['mail'] = 'melike@comu.edu.tr'
    attrs['userPassword'] = generate_passwd()
    ldif = modlist.addModlist(attrs)
    l.add_s(dn,ldif)
    l.unbind_s()


def send_email(html_content,to):
    subject, from_email = 'Kullanici Kaydi', 'akagunduzebru8@gmail.com'
    text_content = 'mesaj icerigi'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    print "mail gonderildi"
    msg.send()

def generate_url_id():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(20)])
    return url_id
