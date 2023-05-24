from django.shortcuts import render
from django.http import HttpResponse

def main_page(request):
    return render(request, 'main/index.html')

def to_home(request):
    return render(request, 'home/index.html')