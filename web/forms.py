from django.forms import ModelForm
from web.models import FirstTimeUser
from captcha.fields import CaptchaField

class FirstTimeUserForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = FirstTimeUser
        fields = ('name', 'middle_name','surname','email','faculty', 'department')
