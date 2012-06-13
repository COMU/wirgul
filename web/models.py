from django.db import models

# Create your models here.

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
    urlid = models.CharField(max_length=100)


class FirstTimeUser(models.Model):
    name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty)
    department = models.ForeignKey(Department)
    email = models.EmailField()
    url = models.ForeignKey(UrlId)


