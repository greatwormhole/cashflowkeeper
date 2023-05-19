from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page),
    path('authentication', include('authentication.urls')),
    path('registration', include('registration.urls'))
]
