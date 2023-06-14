from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', LoginAPIView.as_view(), name = 'login'),
    path('register', RegistrationAPIView.as_view(), name = 'register'),
    path('passrec', PasswordRecoveryView.as_view(), name = 'passrec'),
    path('', include('apps.accounts.api.urls'))
]