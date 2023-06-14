from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.serializers import (
    ValidationError,
    CharField,
    ModelSerializer,
    Serializer,)
from .models import User

class RegistrationSerializer(ModelSerializer):

    password = CharField(max_length = 128, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email',]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(Serializer):

    email = CharField(max_length=255)
    username = CharField(max_length=255, read_only=True)
    password = CharField(max_length=128, write_only=True)
    token = CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)
        token = data.get('token', None)

        if email is None:
            raise ValidationError(
                'An username is required to log in.'
            )

        if password is None:
            raise ValidationError(
                'A password is required to log in.'
            )
        
        if token is None:
            raise InvalidToken(
                'Your token is outdated or deleted'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

class PasswordRecoverySerializer(Serializer):

    email = CharField(max_length=255)

    def validate(self, data):

        email = data.get('email', None)

        if email is None:
            raise ValidationError(
                'An email adress is required to recover password'
            )
        
        return {
            'email': email
        }

    