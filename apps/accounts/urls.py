from django.urls import path, include
from .views import RegistrationAPIView, LoginAPIView

app_name = 'authentication'
urlpatterns = [
    path('login', LoginAPIView.as_view(), name = 'login'),
    path('register', RegistrationAPIView.as_view(), name = 'register'),
    path('', include('apps.accounts.api.urls'))
]