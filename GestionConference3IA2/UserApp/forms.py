from django import forms 
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForms(UserCreationForm):
    class Meta:
        model= User
        fields=['username' , 'first_name' , 'last_name' , 'email' , 'affiliation' , 'nationality' , 'password1' , 'password2']
        widgets={
            'email': forms.EmailInput(attrs={'placeholder': "Entrer votre email"}),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),

        }