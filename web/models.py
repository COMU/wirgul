#! -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError

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
    def name_field_error(value):
        if value == "":
            raise ValidationError('İsminizi Buraya Yazmanız zorunludur')
    name = models.CharField(max_length=50,validators=[name_field_error])
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty)
    department = models.ForeignKey(Department)
    email = models.EmailField(unique=True)
    application = models.DateTimeField(auto_now=True)
    url = models.ForeignKey(UrlId, blank=True, null=True)
    secret = models.ForeignKey(FirstTimeUserSecret, blank=True,null=True)

