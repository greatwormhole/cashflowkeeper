from django.forms import ModelForm, EmailField, PasswordInput
from .models import User

class UserRegisterForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password', 'username']