#! -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils.translation import gettext

class Faculty(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return u'%s' % (self.name)

class Department(models.Model):
    name = models.CharField(max_length=150)
    faculty = models.ForeignKey(Faculty)

    def __unicode__(self):
        return u'%s' % (self.name)

class UrlId(models.Model):
    url_id = models.CharField(max_length=100)

class FirstTimeUserSecret(models.Model):
    passwd_change_time = models.DateTimeField(auto_now=True)

class PasswordChange(models.Model):
    email = models.EmailField(verbose_name=gettext('Mail adresiniz'))

class FirstTimeUser(models.Model):
    name = models.CharField(verbose_name=gettext('İsminiz:'),max_length=50)
    middle_name = models.CharField(verbose_name=gettext('Orta Adiniz:'),max_length=50, null=True, blank=True)
    surname = models.CharField(verbose_name=gettext('Soyadiniz:'),max_length=100)
    faculty = models.ForeignKey(Faculty,verbose_name=gettext('Fakülteniz'))
    department = models.ForeignKey(Department,verbose_name=gettext('Bölümünüz'))
    email = models.EmailField(unique=True,verbose_name=gettext('Mail adresiniz'))
    application = models.DateTimeField(auto_now=True)
    url = models.ForeignKey(UrlId, blank=True, null=True)
    secret = models.ForeignKey(FirstTimeUserSecret, blank=True,null=True)





