from Quiz import models
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm #,UserChangeForm
from django.contrib.auth.models import User

class register_user_form(UserCreationForm):
    class Meta:
        fields = ('username','password1','password2','email')
        model = User
        # widgets = {
        # 'username' : widgets.TextInput(attrs={'class':'form-control'}) ,
        # 'password' : widgets.PasswordInput(attrs={'class':'form-control'}),
        # 'password2' : widgets.PasswordInput(attrs={'class':'form-control'}),
        # 'email':  widgets.TextInput(attrs={'class':'form-control'}),
        # }
        

