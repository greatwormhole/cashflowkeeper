from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .renderers import *
from .forms import *


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer, UserTemplateHTMLRenderer)

    template_name = 'accounts/register_form.html'

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response(serializer.data, status=status.HTTP_201_CREATED)

        return response
    
    def get(self, request):

        form = UserRegisterForm(request.data)
        serializer = self.serializer_class(data=request.data)

        data = {
            'form': form
        }

        response = Response(data, status=status.HTTP_200_OK)

        return response
    
class LoginAPIView(APIView):

    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response
    
    def get(self, request):
        pass
    

class PasswordRecoveryView(APIView):
    
    permission_classes = [AllowAny, ]
    renderer_classes = [UserJSONRenderer, ]
    serializer_class = PasswordRecoverySerializer

    def post(self, request):

        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response

    def get(self, request):
        pass