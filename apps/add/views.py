from django.shortcuts import render, redirect
from .forms import TransactionsForm, EditForm


# Create your views here.
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