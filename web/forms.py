#! -*- coding: utf-8 -*-
from django.forms import ModelForm
from web.models import FirstTimeUser,PasswordChange,GuestUser
from captcha.fields import CaptchaField

class FirstTimeUserForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = FirstTimeUser
        fields = ('name', 'middle_name','surname','email','faculty', 'department')

class PasswordChangeForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = PasswordChange
        fields = ('email',)

class GuestUserForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = GuestUser
        fields = ('name','middle_name','surname','guest_user_email','email','guest_user_phone','type','time_duration')