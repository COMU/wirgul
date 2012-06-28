#! -*- coding: utf-8 -*-
from django.db import models

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
    passwd_change_time = models.DateTimeField()

class FirstTimeUser(models.Model):
    name = models.CharField(verbose_name='İsminiz:',max_length=50)
    middle_name = models.CharField(verbose_name='Orta Adiniz:',max_length=50, null=True, blank=True)
    surname = models.CharField(verbose_name='Soyadiniz:',max_length=100)
    faculty = models.ForeignKey(Faculty,verbose_name='Fakülteniz')
    department = models.ForeignKey(Department,verbose_name='Bölümünüz')
    email = models.EmailField(unique=True,verbose_name='Mail adresiniz')
    application = models.DateTimeField(auto_now=True)
    url = models.ForeignKey(UrlId, blank=True, null=True)
    secret = models.ForeignKey(FirstTimeUserSecret, blank=True,null=True)


