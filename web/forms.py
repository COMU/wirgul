from django.forms import ModelForm
from web.models import FirstTimeUser
from web.models import Faculty

class FirstTimeUserForm(ModelForm):
    class Meta:
        model = FirstTimeUser
        fields = ('name', 'middle_name','surname','email', 'faculty', 'department')



