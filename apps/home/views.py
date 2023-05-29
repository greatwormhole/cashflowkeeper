from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transactions, Category

@login_required(login_url='login')
def home_page(request):
    return render(request, 'home/index.html')

def add(request):
    return render(request, 'home/add.html')

def statistics(request):
    transaction = Transactions.objects.all()
    return render(request, 'home/statistics.html', {'transaction': transaction})

def history(request):
    return render(request, 'home/history.html')

def profile(request):
    return render(request, 'home/profile.html')

def add_category(request):
    return render(request, 'home/add_category.html')
