from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name = 'home'),
    path('add/', views.add, name='add'),
    path('add_category/', views.add_category, name='add_category'),
    path('statistics/', views.statistics, name = 'statistics'),
    path('history/', views.history, name = 'history'),
    path('profile/', views.profile, name = 'profile'),

]
