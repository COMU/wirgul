#! -*- coding: utf-8 -*-
import ldap
import string
from random import choice
from web.models import FirstTimeUser,UrlId,GuestUser,PasswordChange
from django.core.urlresolvers import reverse
from django.conf import settings
from ldapmanager import *
import mail_content
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import status

def guest_user_invalid_request(to):
    subject = 'Misafir Kullanici Bilgilendirme'
    text_content = "mesaj icerigi"
    g = GuestUser.objects.get(email= to)
    name =  " ".join([g.name,g.middle_name,g.surname])
    mail_text = " ".join([mail_content.SN,name,mail_content.GUEST_USER_INVALID_REQUEST,settings.MAIL_FOOTER])
    mail_text = mail_text.encode("utf-8")
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER ,[to])
    msg.attach_alternative(mail_text, "text")
    msg.send()

def host_user_confirm(to,guest_user_email):
    subject = 'Misafir Kullanici Bilgilendirme'
    text_content = "mesaj icerigi"
    f = FirstTimeUser.objects.get(email= to)
    g = GuestUser.objects.get(guest_user_email=guest_user_email)
    guest_name = " ".join([g.name,g.middle_name,g.surname])
    path_ = reverse('password_change_registration', kwargs={'url_id': str(g.url)})
    name =  " ".join([f.name,f.middle_name,f.surname])  # ev sahibi kullanıcının adı soyadı
    mail_text = " ".join(['<html><head>',mail_content.SN,name,guest_name,mail_content.HOST_USER_CONFIRM,'<a href="http://'
        ,settings.SERVER_ADRESS,path_,'">',mail_content.CLICK,'</a><br/><br/>',settings.MAIL_FOOTER,'</head></html>'])
    mail_text = mail_text.encode("utf-8")
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER ,[to])
    msg.attach_alternative(mail_text, "text")
    msg.send()

def guest_user_info(email):
    pass

def ldap_cn(email):
    o = LdapHandler()
    o.connect()
    o.bind()
    return o.get_cn(email)

def guest_user_confirm(to):
    subject = 'Misafir Kullanici Bilgilendirme'
    text_content = "mesaj icerigi"
    f = GuestUser.objects.get(guest_user_email = to)
    name =  " ".join([f.name,f.middle_name,f.surname])
    mail_text = " ".join([mail_content.SN,name,mail_content.GUEST_USER_CONFIIRM,settings.MAIL_FOOTER])
    mail_text = mail_text.encode("utf-8")
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER ,[to])
    msg.attach_alternative(mail_text, "text/html")
    msg.send()

def change_password_confirm(to,url_):
    subject = 'Parola Degisikligi Onaylama'
    text_content = "mesaj icerigi"
    name = ldap_cn(to)  # kullanicinin cn ini almak icin tanımlamanan fonksiyon
    password_obj, created = PasswordChange.objects.get_or_create(url=url_,email=to)
    path_ = reverse('password_change_registration', kwargs={'url_id': url_})
    link = '<a href="http://'+settings.SERVER_ADRESS+path_+'">'+mail_content.CLICK+'</a><br/><br/>'
    mail_text = " ".join(['<html><head>',mail_content.SN,name,mail_content.CHANGE_PASSWORD_CONFIRM,link,settings.MAIL_FOOTER,'</head></html>'])
    mail_text = mail_text.encode("utf-8")
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER ,[to])
    msg.attach_alternative(mail_text, "text/html")
    msg.send()

def change_password_info(to,password):
    subject = 'Parola Değişimi'
    text_content = 'mesaj icerigi'
    name = ldap_cn(to)
    mail_text = " ".join(['<html><head>',mail_content.SN,name,
                          mail_content.CHANGE_PASSWORD_INFO,password,'<br /><br /><br />',settings.MAIL_FOOTER,'</head></html>'])
    mail_text = mail_text.encode("utf-8")
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(mail_text, "text/html")
    msg.send()

def new_user_confirm(to,url_,url_id):
    subject = 'Onaylama'
    text_content = "mesaj icerigi"
    f = FirstTimeUser.objects.get(url=url_id)
    name =  " ".join([f.name,f.middle_name,f.surname])
    path_ = reverse('new_user_registration_view', kwargs={'url_id': url_})
    link = '<a href="http://'+settings.SERVER_ADRESS+path_+'">'+mail_content.LINK+'</a><br/><br/>'
    mail_text = " ".join(['<html><head>',mail_content.SN,name,mail_content.NEW_USER_INFO,link,mail_content.CLICK,'<br /><br />',settings.MAIL_FOOTER,'</head></html>'])
    mail_text = mail_text.encode("utf-8")
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER ,[to])
    msg.attach_alternative(mail_text, "text/html")
    msg.send()

def add_new_user(url,passwd):
    obj = LdapHandler()
    obj.connect()
    obj.bind()
    u = UrlId.objects.get(url_id=url)
    f = FirstTimeUser.objects.get(url=u)
    name = str(f.name)
    middle_name = str(f.middle_name)
    surname=str(f.surname)
    email = str(f.email)
    if obj.add(name,middle_name,surname,email,passwd):  # ldap'a ekleme yapıldıysa true doner
        obj.unbind()
        new_user_info(url,passwd,email)
        return status.ADD_OK
    else: # herhangi bir sorun olusup yeni kullanici kaydi alinamadiysa
        return status.ADD_ERROR


def user_already_exist(to):   # ldap'ta var ama mysql'de kayıtlı degilse
    subject = 'Kullanici Kaydi'
    text_content = 'mesaj icerigi'
    f = FirstTimeUser.objects.get(email = to)
    name = str(f.name)
    middle_name = str(f.middle_name)
    surname = str(f.surname)
    name = " ".join([name,middle_name,surname])
    mail_text = " ".join(['<html><head>',mail_content.SN,name,mail_content.USER_ALREADY_EXIST_TEXT,'<br /><br />',settings.MAIL_FOOTER,'</head></html>'])
    mail_text = mail_text.encode("utf-8")
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(mail_text, "text/html")
    msg.send()

def new_user_info(url,passwd,to):
    subject = 'Kullanici Kaydi'
    text_content = 'mesaj icerigi'
    u = UrlId.objects.get(url_id=url)
    f = FirstTimeUser.objects.get(url=u)
    name = str(f.name)
    middle_name = str(f.middle_name)
    surname=str(f.surname)
    name = " ".join([name,middle_name,surname])
    email = str(f.email)
    if email.find("@gmail.com") != -1:
        mail_adr = email.split("@")
        email = mail_adr[0]
        email = "".join([email,"@comu.edu.tr"])
    mail_text = " ".join(['<html><head>',mail_content.SN,name,mail_content.PASSWORD,
                          passwd,mail_content.USER_NAME,email,'<br /><br /><br />',settings.MAIL_FOOTER,'</head></html>'])
    msg = EmailMultiAlternatives(subject, text_content,settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(mail_text, "text/html")
    msg.send()

def generate_url_id():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(20)])
    return url_id

def generate_passwd():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(5)])
    return url_id

def upper_function(s):
    rep = [ (u'İ',u'I'), (u'Ğ',u'G'),(u'Ü',u'U'), (u'Ş',u'S'), (u'Ö',u'O'),(u'Ç',u'C'),(u'ı',u'i'),(u'ğ',u'g'),(u'ü',u'u'),(u'ş',u's'),(u'ö',u'o'),(u'ç',u'c')]
    for i, i_replace in rep:
        s = s.replace(i, i_replace)
    return s.upper()
