#! -*- coding: utf-8 -*-

import string
import datetime
from random import choice
from web.models import FirstTimeUser,UrlId,GuestUser,PasswordChange
from django.core.urlresolvers import reverse
from django.conf import settings
from ldapmanager import *
import mail_content
from django.core.mail import EmailMultiAlternatives
import smtplib
import random

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
    password_obj, created = PasswordChange.objects.get_or_create(url=url_,email=to,url_create_time=datetime.datetime.now())
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

def send_new_user_confirm(to, generated_url, url_obj):

    f = FirstTimeUser.objects.get(url=url_obj)
    name = ""
    if f.middle_name:
        name =  " ".join([f.name,f.middle_name,f.surname])
    else:
        name = " ".join([f.name, f.surname])

    path = reverse('new_user_registration_view', kwargs={'url_id': generated_url})
    link = "".join([settings.SERVER_ADRESS,path])

    text = mail_content.DEAR + name + "," + "\r\n\r\n"
    text += mail_content.NEW_USER_APPLICATION_TEXT_BODY
    text += "".join(['<a href="', link, '">', mail_content.NEW_USER_LINK_TEXT, "</a>"])
    text += "\r\n\r\n"
    text += settings.TEXT_MAIL_FOOTER
    text = text.encode("utf-8")

    html = "".join([mail_content.NEW_USER_HTML_BODY_STARTS, mail_content.NEW_USER_HTML_DEAR_STARTS, name, mail_content.NEW_USER_HTML_DEAR_ENDS, mail_content.NEW_USER_HTML_BODY_CONTENT])
    html += "".join(['<a href="', link, '">', mail_content.NEW_USER_LINK_TEXT, "</a>"])
    html += "<br /><br />"
    html += settings.HTML_MAIL_FOOTER
    html = html.encode("utf-8")

    subject = mail_content.NEW_USER_APPLICATION_SUBJECT
    message = createhtmlmail(html, text, subject, settings.EMAIL_FROM_DETAIL)
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.set_debuglevel(1)
    if settings.EMAIL_USE_TLS:
        server.starttls()
    try:
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        rtr_code =  server.verify(to)
        server.sendmail(settings.EMAIL_FROM, to, message)
        server.quit()
        #print rtr_code
        return rtr_code[0]
    except:
        return False



    mail_text = " ".join(['<html><head>',mail_content.SN,name,mail_content.NEW_USER_INFO,link,mail_content.CLICK,'<br /><br />',settings.MAIL_FOOTER,'</head></html>'])
    mail_text = mail_text.encode("utf-8")
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER ,[to])
    msg.attach_alternative(mail_text, "text/html")
    msg.send()

def add_new_user(url, passwd, ldap_handler):
    u = UrlId.objects.get(url_id=url)
    f = FirstTimeUser.objects.get(url=u)
    name = str(f.name)
    middle_name = str(f.middle_name)
    surname=str(f.surname)
    email = str(f.email)
    if ldap_handler.add(name, middle_name, surname, email, passwd):  # ldap'a ekleme yapıldıysa true doner
        send_new_user_info(u, passwd, email)
        return TRUE
    else: # herhangi bir sorun olusup yeni kullanici kaydi alinamadiysa
        return FALSE


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

def send_new_user_info(url, passwd, to):
    f = FirstTimeUser.objects.get(url=url)
    email = f.email
    #if email.find("@gmail.com") != -1:
    #    mail_adr = email.split("@")
    #    email = mail_adr[0]
    #    email = "".join([email,"@comu.edu.tr"])

    name = ""
    if f.middle_name:
        name =  " ".join([f.name,f.middle_name,f.surname])
    else:
        name = " ".join([f.name, f.surname])

    link = settings.EDUROAM_INFO_LINK

    text = mail_content.DEAR + name + "," + "\r\n\r\n"
    text += mail_content.NEW_USER_LOGIN_DETAILS_TEXT_BODY
    text += " ".join(mail_content.NEW_USER_LOGIN_DETAILS_USERNAME, email, "\r\n", mail_content.NEW_USER_LOGIN_DETAILS_PASSWORD, passwd, "\r\n")
    text += mail_content.NEW_USER_LOGIN_DETAILS_EDUROAM_PAGE
    text += "".join(["<a href=\"", settings.EDUROAM_INFO_ADDRESS, "\">", settings.EDUROAM_INFO_ADDRESS, "</a>"])
    text += "\r\n\r\n"
    text += settings.TEXT_MAIL_FOOTER
    text = text.encode("utf-8")

    html = "".join([mail_content.NEW_USER_HTML_BODY_STARTS, mail_content.NEW_USER_HTML_DEAR_STARTS, name, mail_content.NEW_USER_HTML_DEAR_ENDS, mail_content.NEW_USER_LOGIN_DETAILS_HTML_BODY_CONTENT])
    htl += " ".join([mail_content.NEW_USER_LOGIN_DETAILS_HTML_USERNAME, email, "<br/>", mail_content.NEW_USER_LOGIN_DETAILS_HTML_PASSWORD, passwd, "<br/>"])
    html += "".join(['<a href="', link, '">', mail_content.NEW_USER_LINK_TEXT, "</a>"])
    html += "<br /><br />"
    html += settings.HTML_MAIL_FOOTER
    html = html.encode("utf-8")

    subject = mail_content.NEW_USER_LOGIN_DETAILS_SUBJECT
    message = createhtmlmail(html, text, subject, settings.EMAIL_FROM_DETAIL)
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.set_debuglevel(1)
    if settings.EMAIL_USE_TLS:
        server.starttls()
    try:
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        rtr_code =  server.verify(to)
        server.sendmail(settings.EMAIL_FROM, to, message)
        server.quit()
        #print rtr_code
        return rtr_code[0]
    except:
        return False

def generate_url_id():
    url_id = ''.join([choice(string.letters + string.digits) for i in range(20)])
    return url_id

def generate_passwd(min_length=6, max_length=10):
    length1=random.randint(min_length,max_length)
    letters=string.ascii_letters+string.digits
    use0 = letters.partition("l")
    part = use0[2]
    use1 = part.partition("o")
    part = use1[2]
    use2 = part.partition("I")
    part = use2[2]
    use3 = part.partition("O")
    part = use3[2]
    use4 = part.partition("0")
    letters = "".join([use0[0], use1[0], use2[0], use3[0], use4[0], use4[2]])
    letters = letters.partition("-")[0]
    return ''.join([random.choice(letters) for _ in range(length1)])

def upper_function(s):
    rep = [ (u'İ',u'I'), (u'Ğ',u'G'),(u'Ü',u'U'), (u'Ş',u'S'), (u'Ö',u'O'),(u'Ç',u'C'),(u'ı',u'i'),(u'ğ',u'g'),(u'ü',u'u'),(u'ş',u's'),(u'ö',u'o'),(u'ç',u'c')]
    for i, i_replace in rep:
        s = s.replace(i, i_replace)
    return s.upper()

def createhtmlmail (html, text, subject, fromEmail):
    """Create a mime-message that will render HTML in popular
    MUAs, text in better ones"""
    import MimeWriter
    import mimetools
    import cStringIO

    out = cStringIO.StringIO() # output buffer for our message
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)

    writer = MimeWriter.MimeWriter(out)
    #
    # set up some basic headers... we put subject here
    # because smtplib.sendmail expects it to be in the
    # message body
    #
    writer.addheader("From", fromEmail)
    writer.addheader("Subject", subject)
    writer.addheader("MIME-Version", "1.0")
    #
    # start the multipart section of the message
    # multipart/alternative seems to work better
    # on some MUAs than multipart/mixed
    #
    writer.startmultipartbody("alternative")
    writer.flushheaders()
    #
    # the plain text section
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'utf-8')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()
    #
    # start the html subpart of the message
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    #
    # returns us a file-ish object we can write to
    #
    pout = subpart.startbody("text/html", [("charset", 'utf-8')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()
    #
    # Now that we're done, close our writer and
    # return the message body
    #
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    #print msg
    return msg
