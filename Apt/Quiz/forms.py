from .models import questions,parameters,exam
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm #,UserChangeForm
from django.contrib.auth.models import User

from Quiz import models

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
        
class add_questions_form(ModelForm):
    class Meta:
        fields = '__all__'
        model = questions
        labels = {
            'parameter':'Parameter for option A'
        }

class add_parameters_form(ModelForm):
    class Meta:
        fields = '__all__'
        model = parameters

class add_exam_form(ModelForm):
    class Meta:
        fields = '__all__'
        model = exam


