#! -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from web.models import FirstTimeUser,PasswordChange,GuestUser
from captcha.fields import CaptchaField
from django.conf import settings

from wirgul.utils.messages import INVALID_EMAIL_FORM_MESSAGE, REQUIRED_FORM_MESSAGE, \
    INVALID_CAPTCHA_FORM_MESSAGE, INVALID_DOMAIN_EMAIL, INVALID_GUEST_EMAIL, INVALID_CITIZEN_NO

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

    def clean_email(self):
        domain = settings.EDUROAM_DOMAIN
        exception_domain = settings.EDUROAM_EXCEPTION_DOMAIN
        student_domain = settings.STUDENT_DOMAIN
        data = self.cleaned_data['email']
        mail_li = data.split("@")
        if domain != mail_li[1] and exception_domain != mail_li[1] and student_domain != mail_li[1]:
            raise forms.ValidationError(INVALID_DOMAIN_EMAIL)

        return data

class PasswordChangeForm(ModelForm):
    captcha = CaptchaField()
    def __init__(self,*args,**kwargs):
        super(PasswordChangeForm,self).__init__(*args,**kwargs)
        self.fields['email'].error_messages = {'invalid': INVALID_EMAIL_FORM_MESSAGE,'required': REQUIRED_FORM_MESSAGE}
        self.fields['captcha'].error_messages = {'required': REQUIRED_FORM_MESSAGE, 'invalid': INVALID_CAPTCHA_FORM_MESSAGE}
    class Meta:
        model = PasswordChange
        fields = ('email',)

    def clean_email(self):
        domain = settings.EDUROAM_DOMAIN
        exception_domain = settings.EDUROAM_EXCEPTION_DOMAIN
        student_domain = settings.STUDENT_DOMAIN
        data = self.cleaned_data['email']
        mail_li = data.split("@")
        if domain != mail_li[1] and exception_domain != mail_li[1] and student_domain != mail_li[1]:
            raise forms.ValidationError(INVALID_DOMAIN_EMAIL)

        return data

class GuestUserForm(ModelForm):
    captcha = CaptchaField()
    def __init__(self,*args,**kwargs):
        super(GuestUserForm,self).__init__(*args,**kwargs)
        self.fields['name'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['email'].error_messages = {'invalid': INVALID_EMAIL_FORM_MESSAGE, 'required': REQUIRED_FORM_MESSAGE}
        self.fields['guest_user_email'].error_messages = {'invalid': INVALID_EMAIL_FORM_MESSAGE,'required': REQUIRED_FORM_MESSAGE}
        self.fields['surname'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['citizen_no'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['type'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['time_duration'].error_messages = {'required': REQUIRED_FORM_MESSAGE}
        self.fields['captcha'].error_messages = {'required': REQUIRED_FORM_MESSAGE, 'invalid': INVALID_CAPTCHA_FORM_MESSAGE}
    class Meta:
        model = GuestUser
        fields = ('name','middle_name','surname','citizen_no','guest_user_email','email','guest_user_phone','type','time_duration')

    # kullanıcının herhangi bir eposta girmesine izin veriliyor
#    def clean_guest_user_email(self): #belli bir yetkilendirici veya alan adı ile uyumlu epostalar geçerlidir
#        data = self.cleaned_data['guest_user_email']
#        email_parts = data.split(".")
#        if ("edu") not in email_parts:
#            raise forms.ValidationError(INVALID_GUEST_EMAIL)
#
#        return data

    def clean_email(self):
        eduroam_control_domain_li = list(settings.EDUROAM_CONTROL_EMAIL)
        data = self.cleaned_data['email']
        if data not in eduroam_control_domain_li:
            raise forms.ValidationError(INVALID_DOMAIN_EMAIL)
#        domain = settings.EDUROAM_DOMAIN
#        exception_domain = settings.EDUROAM_EXCEPTION_DOMAIN
#        student_domain = settings.STUDENT_DOMAIN
#        data = self.cleaned_data['email']
#        mail_li = data.split("@")
#        if domain != mail_li[1] and exception_domain != mail_li[1] and student_domain != mail_li[1]:
#            raise forms.ValidationError(INVALID_DOMAIN_EMAIL)

        return data

    def clean_citizen_no(self):
        data = self.cleaned_data['citizen_no']
        if len(data) != 11:
            raise forms.ValidationError(INVALID_CITIZEN_NO)

        try:
            int(data)
        except ValueError:
            raise forms.ValidationError(INVALID_CITIZEN_NO)

        if int(data[0]) == 0:
            raise forms.ValidationError(INVALID_CITIZEN_NO)

        # 1. 3. 5. 7. ve 9. hanelerin toplamının 7 katından, 2. 4. 6. ve 8. hanelerin toplamı çıkartıldığında, elde edilen sonucun 10'a bölümünden kalan, yani Mod10'u bize 10. haneyi verir
        odds = reduce(lambda x, y: int(x)+int(y), [data[0], data[2], data[4], data[6], data[8]])
        evens = reduce(lambda x, y: int(x)+int(y), [data[1], data[3], data[5], data[7]])

        if (odds * 7 - evens) % 10 != int(data[9]):
            raise forms.ValidationError(INVALID_CITIZEN_NO)

        # 1. 2. 3. 4. 5. 6. 7. 8. 9. ve 10. hanelerin toplamından elde edilen sonucun 10'a bölümünden kalan, yani Mod10'u bize 11. haneyi verir.

        alls = reduce(lambda x, y: int(x)+int(y), data[:10])

        if alls % 10 != int(data[10]):
            raise forms.ValidationError(INVALID_CITIZEN_NO)

        return data

