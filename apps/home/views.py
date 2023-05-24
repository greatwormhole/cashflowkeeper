from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home_page(request):
    return render(request, 'home/index.html')

def add(request):
    return render(request, 'home/add.html')

def statistics(request):
    return render(request, 'home/statistics.html')

def history(request):
    return render(request, 'home/history.html')

def profile(request):
    return render(request, 'home/profile.html')