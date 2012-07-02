#! -*- coding: utf-8 -*-
import ldap
import string
from random import choice
import ldap.modlist as modlist
from web.models import FirstTimeUser,UrlId
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def send_email_confirm(to,url_):
    subject, from_email = 'Onaylama', 'akagunduzebru8@gmail.com'
    text_content = "mesaj icerigi"
    html_content = '<html><head>'+"Kullanıcı adı ve parola bilgilerinizi alabilmek için aşagıdaki linke"
    path_ = reverse('new_user_registration_view', kwargs={'url_id': url_})
    html_content +='<p><a href="http://127.0.0.1:8000'+path_+'">TIKLAYINIZ </a></head></html>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def generate_passwd():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(5)])
    return url_id

def ldap_add_new_user(request,user_passwd):
    l = ldap.open("127.0.0.1")
    l.protocol_version = ldap.VERSION3
    username = "cn=admin, dc=comu,dc=edu,dc=tr"
    password  = "ldap123"
    l.simple_bind_s(username, password)
    array_obj = FirstTimeUser.objects.values_list('name','middle_name','surname','email')
    f = FirstTimeUser.objects.all()
    length = f.count() - 1
    dn="mail="+str(array_obj[length][0])+str(array_obj[length][1])+\
       str(array_obj[length][2])+"@comu.edu.tr,ou=personel,ou=people,dc=comu,dc=edu,dc=tr"
    attrs = {}
    attrs['objectclass'] = ['organizationalPerson','person','inetOrgPerson']
    attrs['givenName'] = str(array_obj[length][0])+" " + str(array_obj[length][1])
    attrs['sn'] = str(array_obj[length][2])
    attrs['cn'] = str(array_obj[length][0]) +" "+ str(array_obj[length][1]) +" " + str(array_obj[length][2])
    attrs['mail'] =str(array_obj[length][0])+str(array_obj[length][1])+str(array_obj[length][2])+'@comu.edu.tr'
    attrs['userPassword'] = user_passwd
    ldif = modlist.addModlist(attrs)
    print "ldap"
    l.add_s(dn,ldif)
    l.unbind_s()

def send_email_passwd(email):
    user_passwd = generate_passwd()
    subject, from_email = 'Parola Değişimi', 'akagunduzebru8@gmail.com'
    text_content = 'mesaj icerigi'
    url_ = generate_url_id()
    path_ = reverse('new_user_registration_view', kwargs={'url_id': url_})
    date_obj = FirstTimeUser.objects.get(email= email)
    time = str(date_obj.application)
    name = str(date_obj.name+" "+date_obj.middle_name+" "+date_obj.surname)
    html_content = '<html><head>'+"Sayin "+name+" en son "+time+" tarihinde parolanızı aldınız."+'<p>'+"Yeni parolanız: "
    html_content +=user_passwd
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def send_email(new_user_p,to):
    subject, from_email = 'Kullanici Kaydi', 'akagunduzebru8@gmail.com'
    text_content = 'mesaj icerigi'
    array_obj = FirstTimeUser.objects.values_list('name','middle_name','surname','email')
    f = FirstTimeUser.objects.all()
    length = f.count() - 1
    url_obj = UrlId.objects.values_list('url_id')
    u = UrlId.objects.all()
    length_u = u.count()-1
    path_ = reverse('new_user_registration_view', kwargs={'url_id':str(url_obj[length_u][0])})
    html_content ='<html><head>'+"Sayin "+str(array_obj[length][0]) +" "\
                  + str(array_obj[length][1]) +" " + str(array_obj[length][2])+"\n"
    html_content += '<p>'+"Kullanıcı Mail Adresiniz: "+str(array_obj[length][0])+str(array_obj[length][1])+str(array_obj[length][2])+'@comu.edu.tr'
    html_content +='<p>'+"Parolanız: "+new_user_p+"\n"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def generate_url_id():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(20)])
    return url_id


