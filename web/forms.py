#! -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms import forms
from django import forms
from web.models import FirstTimeUser,PasswordChange,GuestUser
from captcha.fields import CaptchaField

class FirstTimeUserForm(ModelForm):
    captcha = CaptchaField()
    def __init__(self,*args,**kwargs):
        super(FirstTimeUserForm,self).__init__(*args,**kwargs)
        self.fields['name'].error_messages = {'required': 'Bu alani doldurmak zorundasiniz.'}
        self.fields['email'].error_messages = {'invalid': 'Gecersiz bir eposta adresi girdiniz.','required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['surname'].error_messages = {'required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['faculty'].error_messages = {'required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['department'].error_messages = {'required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['captcha'].error_messages = {'required':'Bu alani doldurmak zorundasiniz.','invalid':'Captcha yi yanlis girdiniz'}
    class Meta:
        model = FirstTimeUser
        fields = ('name', 'middle_name','surname','email','faculty', 'department')

"""
class ModelForm (ModelForm):
    class Meta:
        model = FirstTimeUser

    def __init__(self, *args, **kwargs):
        super(FirstTimeUser, self).__init__(*args, **kwargs)
        self.fields['field'].error_messages={'required': 'custom message'}
"""

class PasswordChangeForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = PasswordChange
        def __init__(self,*args,**kwargs):
            super(PasswordChangeForm,self).__init__(*args,**kwargs)
            self.fields['email'].error_messages = {'invalid': 'Gecersiz bir eposta adresi girdiniz.','required':'Bu alani doldurmak zorundasiniz.'}
        fields = ('email',)

class GuestUserForm(ModelForm):
    captcha = CaptchaField()
    def __init__(self,*args,**kwargs):
        super(GuestUserForm,self).__init__(*args,**kwargs)
        self.fields['name'].error_messages = {'required': 'Bu alani doldurmak zorundasiniz.'}
        self.fields['email'].error_messages = {'invalid': 'Gecersiz bir eposta adresi girdiniz.','required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['guest_user_email'].error_messages = {'invalid': 'Gecersiz bir eposta adresi girdiniz.','required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['surname'].error_messages = {'required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['type'].error_messages = {'required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['time_duration'].error_messages = {'required':'Bu alani doldurmak zorundasiniz.'}
        self.fields['captcha'].error_messages = {'required':'Bu alani doldurmak zorundasiniz.','invalid':'Captcha yi yanlis girdiniz'}
    class Meta:
        model = GuestUser
        fields = ('name','middle_name','surname','guest_user_email','email','guest_user_phone','type','time_duration')