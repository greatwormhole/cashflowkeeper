from django.urls import path, include
from django.contrib.auth import urls as auth_urls
from . import views
from apps.accounts import views as account_views
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('', views.main_page, name = 'main'),
]
