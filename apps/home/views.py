from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transactions, Category
from .forms import TransactionsForm, EditForm
from django.db.models import Sum
import pandas as pd
import datetime
import json

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
    # работа с датами
    dates_list = Transactions.objects.values_list('date')
    min_date = dates_list.order_by('date').first()[0]
    max_date = dates_list.order_by('date').last()[0]
    min_date_str = dates_list.order_by('date').first()[0].strftime("%Y-%m-%d")
    max_date_str = dates_list.order_by('date').last()[0].strftime("%Y-%m-%d")

    # работа с транзакциями
    transaction = Transactions.objects.values('date', 'type').order_by().annotate(amount=Sum('amount')).order_by('date')
    transaction = list(transaction)
    # приведение дат к строке
    for item in transaction:
        item['date'] = item['date'].strftime("%Y-%m-%d")

    # заполнение пропущенных дат нулями
    all_dates_list = pd.date_range(min_date, max_date).strftime("%Y-%m-%d").to_list()

    for el in all_dates_list:
        transaction.append({'date': el, 'type': 'Income', 'amount': 0})
        transaction.append({'date': el, 'type': 'Outcome', 'amount': 0})
        transaction.append({'date': el, 'type': 'Investment', 'amount': 0})

    transaction_json = json.dumps(transaction)
    transaction_df = pd.read_json(transaction_json)
    transaction_df['date'] = transaction_df['date'].dt.strftime("%Y-%m-%d")

    # группировка датафрейма
    transaction_df = transaction_df.groupby(['date', 'type'], as_index=False).agg(sum_of_amount=('amount', 'sum')).sort_values(by='date')
    transaction_json = transaction_df.to_json(orient='records')
    transaction = json.loads(transaction_json)
    return render(request, 'home/statistics.html', {'transaction': transaction, 'min_date': min_date_str, 'max_date': max_date_str})


def history(request):
    return render(request, 'home/history.html')

def profile(request):
    return render(request, 'home/profile.html')
