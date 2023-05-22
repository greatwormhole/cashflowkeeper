from django.shortcuts import render
from django.http import HttpResponse

def main_page(request):
    return render(request, 'main/index.html')

def sign_in(request):
    return render(request, 'main/auth.html')

def sign_up(request):
    return render(request, 'main/reg.html')

def pass_recovery(request):
    return render(request, 'main/pass_rec.html')

def to_home(request):
    return render(request, 'home/index.html')