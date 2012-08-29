#! -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext
from django.conf import settings

from wirgul.utils.messages import WEB_MODEL_EMAIL, WEB_MODEL_MIDDLE_NAME, WEB_MODEL_SURNAME, WEB_MODEL_YOURNAME, \
    WEB_MODEL_FACULTY, WEB_MODEL_DEPARTMENT, WEB_MODEL_GUEST_EMAIL, WEB_MODEL_CHOOSE_DURATION_TYPE, \
    WEB_MODEL_CHOOSE_DURATION, WEB_MODEL_TEL_NUMBER

class Faculty(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return u'%s' % (self.name)

class Department(models.Model):
    name = models.CharField(max_length=150)
    faculty = models.ForeignKey(Faculty)

    def __unicode__(self):
        return u'%s' % (self.name)

class Url(models.Model):
    url_id = models.CharField(max_length=100)
    url_create_time = models.DateTimeField(auto_now=True) # urlin ilk oluşturulduğu zaman
    status = models.BooleanField(default=False) # url e tıklama durumu kontrolü

class FirstTimeUserSecret(models.Model):
    passwd_change_time = models.DateTimeField(auto_now=True)

class PasswordChange(models.Model):
    email = models.EmailField(verbose_name=gettext(WEB_MODEL_EMAIL))
    url = models.ForeignKey(Url, blank=True, null=True)

class FirstTimeUser(models.Model):
    name = models.CharField(verbose_name=gettext(WEB_MODEL_YOURNAME),max_length=50)
    middle_name = models.CharField(verbose_name=gettext(WEB_MODEL_MIDDLE_NAME),max_length=50, null=True, blank=True)
    surname = models.CharField(verbose_name=gettext(WEB_MODEL_SURNAME),max_length=100)
    faculty = models.ForeignKey(Faculty,verbose_name=gettext(WEB_MODEL_FACULTY))
    department = models.ForeignKey(Department,verbose_name=gettext(WEB_MODEL_DEPARTMENT))
    email = models.EmailField(verbose_name=gettext(WEB_MODEL_EMAIL))
    url = models.ForeignKey(Url, blank=True, null=True)
    secret = models.ForeignKey(FirstTimeUserSecret, blank=True,null=True)

class GuestUser(models.Model):
    name = models.CharField(verbose_name=gettext(WEB_MODEL_YOURNAME),max_length=50)
    middle_name = models.CharField(verbose_name=gettext(WEB_MODEL_MIDDLE_NAME),max_length=50, null=True, blank=True)
    surname = models.CharField(verbose_name=gettext(WEB_MODEL_SURNAME),max_length=100)
    guest_user_email = models.EmailField(verbose_name=gettext(WEB_MODEL_EMAIL))
    email = models.EmailField(verbose_name=gettext(WEB_MODEL_GUEST_EMAIL))
    guest_user_phone = models.IntegerField(WEB_MODEL_TEL_NUMBER, max_length=10)
    url = models.ForeignKey(Url, blank=True, null=True)
    TIME_CHOICES = (
        (1, 'SAAT'),
        (2, 'GUN'),
        (3, 'HAFTA'),
        )
    type = models.CharField(blank=True,null=True,choices=TIME_CHOICES,default=1,max_length=10,verbose_name=gettext(WEB_MODEL_CHOOSE_DURATION_TYPE))
    time_duration = models.CharField(blank=True,null=True,choices=settings.TIME_DURATION_CHOICES,verbose_name=WEB_MODEL_CHOOSE_DURATION, max_length=10)