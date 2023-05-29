from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transactions, Category
from .forms import TransactionsForm, EditForm


@login_required(login_url='login')
def home_page(request):
    return render(request, 'home/index.html')

def add(request):
    error = ''
    if request.method == 'POST':
        form = TransactionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'

    form = TransactionsForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'home/add.html', data)

def add_category(request):
    error = ''
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'

    form = EditForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'home/add_category.html', data)

def statistics(request):
    transaction = Transactions.objects.all()
    return render(request, 'home/statistics.html', {'transaction': transaction})

def history(request):
    return render(request, 'home/history.html')

def profile(request):
    return render(request, 'home/profile.html')
