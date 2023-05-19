from django.shortcuts import render
from django.http import HttpResponse 

def sign_in(request):
    return HttpResponse("Введите логин и пароль/Забыли пароль")

def pass_recovery(request):
    return HttpResponse("Введите почту для восстановления пароля")