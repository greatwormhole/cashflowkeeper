from django.forms import (
    ModelForm,
    EmailInput,
    PasswordInput,
    TextInput,)
from .models import User

class UserRegisterForm(ModelForm):

    class Meta:

        model = User
        fields = ['email', 'password', 'username']
        widgets = {
            'email': EmailInput(attrs={
                'placeholder': 'email'
            }),
            'password': PasswordInput(attrs={
                'placeholder': 'password'
            }),
            'username': TextInput(attrs={
                'placeholder': 'username'
            }),
        }

class UserLoginForm(ModelForm):

    class Meta:

        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={
                'placeholder': 'username'
            }),
            'password': PasswordInput(attrs={
                'placeholder': 'password'
            }),
        }

class UserPassRecForm(ModelForm):
    
    class Meta:

        model = User
        fields = ['email']
        widgets = {
            'email': EmailInput(attrs={
                'placeholder': 'email'
            })
        }