#! -*- coding: utf-8 -*-
from django.forms import ModelForm
from web.models import FirstTimeUser,PasswordChange,GuestUser
from captcha.fields import CaptchaField

from wirgul.utils.messages import INVALID_EMAIL_FORM_MESSAGE, REQUIRED_FORM_MESSAGE, INVALID_CAPTCHA_FORM_MESSAGE

class FirstTimeUserForm(ModelForm):
    captcha = CaptchaField()
    def __init__(self,*args,**kwargs):
        super(FirstTimeUserForm,self).__init__(*args,**kwargs)
        self.fields['name'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['email'].error_messages = {'invalid': INVALID_EMAIL_FORM_MESSAGE, 'required': REQUIRED_FORM_MESSAGE}
        self.fields['surname'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['faculty'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['department'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['captcha'].error_messages = {'required': REQUIRED_FORM_MESSAGE, 'invalid': INVALID_CAPTCHA_FORM_MESSAGE}
    class Meta:
        model = FirstTimeUser
        fields = ('name', 'middle_name','surname','email','faculty', 'department')

class PasswordChangeForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = PasswordChange
        def __init__(self,*args,**kwargs):
            super(PasswordChangeForm,self).__init__(*args,**kwargs)
            self.fields['email'].error_messages = {'invalid': INVALID_EMAIL_FORM_MESSAGE,'required': REQUIRED_FORM_MESSAGE}
        fields = ('email',)

class GuestUserForm(ModelForm):
    captcha = CaptchaField()
    def __init__(self,*args,**kwargs):
        super(GuestUserForm,self).__init__(*args,**kwargs)
        self.fields['name'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['email'].error_messages = {'invalid': INVALID_EMAIL_FORM_MESSAGE, 'required': REQUIRED_FORM_MESSAGE}
        self.fields['guest_user_email'].error_messages = {'invalid': INVALID_EMAIL_FORM_MESSAGE,'required': REQUIRED_FORM_MESSAGE}
        self.fields['surname'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['type'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['time_duration'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['captcha'].error_messages = {'required': REQUIRED_FORM_MESSAGE, 'invalid': INVALID_CAPTCHA_FORM_MESSAGE}
    class Meta:
        model = GuestUser
        fields = ('name','middle_name','surname','guest_user_email','email','guest_user_phone','type','time_duration')