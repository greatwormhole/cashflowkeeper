from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name = 'main'),
    path('authentication', views.sign_in, name = 'authorisation'),
    path('authentication/passwordrecovery', views.pass_recovery, name = 'passwordrecovery'),
    path('registration', views.sign_up, name = 'registration')
]
