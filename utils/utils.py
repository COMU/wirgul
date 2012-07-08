#! -*- coding: utf-8 -*-
import ldap
import string
from random import choice
from web.models import FirstTimeUser,UrlId
from django.core.urlresolvers import reverse
from django.conf import settings
from ldapmanager import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def send_email_forget_password(to,url_):
    subject = 'Parola Degisikligi'
    text_content = "mesaj icerigi"
    f = FirstTimeUser.objects.get(email= to)
    name =  " ".join([f.name,f.middle_name,f.surname])
    html_content = '<html><head>'+"SAYIN "+name+" KULLANICI ADI VE PAROLA BILGILERINIZI ALABILMEK ICIN ASAGIDAKI LINKE "
    path_ = reverse('password_change_registration', kwargs={'url_id': url_})
    html_content +='<p><a href="http://127.0.0.1:8000'+path_+'">TIKLAYINIZ </a><br/><br/>'
    html_content += settings.MAIL_FOOTER+'</head></html>'
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER ,[to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def forget_password_info(to,password):
    subject = 'Parola Değişimi'
    text_content = 'mesaj icerigi'
    email_obj = FirstTimeUser.objects.get(email= to)
    name = str(email_obj.name+" "+email_obj.middle_name+" "+email_obj.surname)
    html_content = '<html><head>'+"Sayin "+name+'<p>'+"Yeni parolanız: "
    html_content += password + '<br /><br /><br />'
    html_content += settings.MAIL_FOOTER
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_email_confirm(to,url_,url_id):
    subject = 'Onaylama'
    text_content = "mesaj icerigi"
    f = FirstTimeUser.objects.get(url=url_id)
    name =  " ".join([f.name,f.middle_name,f.surname])
    html_content = '<html><head>'+"SAYIN "+name+" KULLANICI ADI VE PAROLA BILGILERINIZI ALABILMEK ICIN ASAGIDAKI LINKE "
    path_ = reverse('new_user_registration_view', kwargs={'url_id': url_})
    html_content +='<p><a href="http://127.0.0.1:8000'+path_+'">TIKLAYINIZ </a><br/><br/>'
    html_content += settings.MAIL_FOOTER+'</head></html>'
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER ,[to])
    msg.attach_alternative(html_content, "text/html")
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
    if obj.search(email) == 1:
        send_email_already_exist(email,u)
        obj.unbind()
        return 1
    obj.add(name,middle_name,surname,email,passwd)
    obj.unbind()
    send_email_info(url,passwd,email)
    return 2

def send_email_already_exist(to,url):   # ldap'ta var ama mysql'de kayıtlı degilse
    subject = 'Kullanici Kaydi'
    text_content = 'mesaj icerigi'
    f = FirstTimeUser.objects.get(url=url)
    name = str(f.name)
    middle_name = str(f.middle_name)
    surname = str(f.surname)
    name = " ".join([name,middle_name,surname])
    html_content = '<html><head>'+"Sayin "+name+" "+" sistemimizde zaten kayıtlısınız."+'<br />'+"Parolanızı unuttuysanız"
    html_content +=" sitemizdeki diğer menülerden yararlanabilirsiniz"
    html_content += '<br /><br />'+settings.MAIL_FOOTER+'</head></html>'
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_change_password():
    pass




def send_email_change_passwd(to):
    user_passwd = generate_passwd()
    l = ldap.open("127.0.0.1")
    l.protocol_version = ldap.VERSION3
    username = "cn=admin, dc=comu,dc=edu,dc=tr"
    password  = "ldap123"
    l.simple_bind_s(username, password)
    mod_attrs = [( ldap.MOD_REPLACE, 'userPassword', '1234' )]
    ldap_mail_adr=""
    for i in to:
        if i == "@":
            break
        ldap_mail_adr +=i
    l.modify_s('mail='+ldap_mail_adr+'@comu.edu.tr,ou=personel,ou=people,dc=comu,dc=edu,dc=tr',mod_attrs)
    subject, from_email = 'Parola Değişimi', 'akagunduzebru8@gmail.com'
    text_content = 'mesaj icerigi'
    email_obj = FirstTimeUser.objects.get(email= to)
    name = str(email_obj.name+" "+email_obj.middle_name+" "+email_obj.surname)
    html_content = '<html><head>'+"Sayin "+name+'<p>'+"Yeni parolanız: "
    html_content +=user_passwd
    html_content += settings.MAIL_FOOTER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_email_info(url,passwd,to):
    subject = 'Kullanici Kaydi'
    text_content = 'mesaj icerigi'
    path_ = reverse('new_user_registration_view', kwargs={'url_id':url})
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
    html_content = '<html><head>'+"Sayin "+name+" Parolaniz : "+passwd+'<br />'
    html_content += 'Kullanici Adiniz : '+ email+'<br /><br /><br />'
    html_content += settings.MAIL_FOOTER+'</head></html>'
    msg = EmailMultiAlternatives(subject, text_content,settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def generate_url_id():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(20)])
    return url_id

def generate_passwd():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(5)])
    return url_id

def upper_function(string):
    rep = [ ('İ','I'), ('Ğ','G'),('Ü','U'), ('Ş','S'), ('Ö','O'),('Ç','C'),('ı','i'),('ğ','g'),('ü','u'),('ş','s'),('ö','o'),('ç','c'),(' ','_')]
    for i, i_replace in rep:
        string = string.replace(i, i_replace)
    return string.upper()
