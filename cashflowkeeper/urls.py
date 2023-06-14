from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls')),
    path('api/', include('apps.accounts.urls')),
    path('home/', include('apps.home.urls')),
]
