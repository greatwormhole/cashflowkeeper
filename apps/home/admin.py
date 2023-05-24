from django.contrib import admin
from .models import *

admin.site.register(Transactions)
admin.site.register(History)
admin.site.register(Profile)
admin.site.register(Statistics)