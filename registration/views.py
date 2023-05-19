from django.shortcuts import render
from django.http import HttpResponse

def sign_up(request):
    return HttpResponse("Введите логин->Введите пароль->Повторите пароль")