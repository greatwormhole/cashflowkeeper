from django.urls import path, include
from django.contrib.auth import urls as auth_urls
from . import views
from apps.accounts import views as account_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('', views.main_page, name = 'main'),
    path('auth/', include(auth_urls)),
    path('login/', account_views.loginPage, name = 'login'),
    path('logout/', account_views.logoutPage, name = 'logout'),
    path('register/', account_views.registerPage, name = 'register'),
    path('passwordrecovery/', account_views.passrecPage, name = 'passwordrecovery'),
    # path('authorisation/passwordrecovery/', views.pass_recovery, name = 'passwordrecovery'),
    # path('register/', views.sign_up, name = 'register'),

    # User registration and authentication through JWT
    path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
