from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('', views.main_page, name = 'main'),
    path('authorisation/', views.sign_in, name = 'authorisation'),
    path('authorisation/passwordrecovery/', views.pass_recovery, name = 'passwordrecovery'),
    path('register/', views.sign_up, name = 'register'),

    # User registration and authentication through JWT
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
