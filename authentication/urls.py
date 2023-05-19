from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('/passwordrecovery', views.pass_recovery)
]
