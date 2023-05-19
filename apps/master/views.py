from django.shortcuts import render
from django.http import HttpResponse

def main_page(request):
    return render(request, 'master/index.html')

def sign_in(request):
    return render(request, 'master/auth.html')

def sign_up(request):
    return render(request, 'master/reg.html')

def pass_recovery(request):
    return render(request, 'master/pass_rec.html')