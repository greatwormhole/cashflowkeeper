from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transactions, Category
from .forms import TransactionsForm, EditForm
from django.db.models import Sum, Q, Count
import pandas as pd
import datetime
from datetime import datetime
import json

@login_required(login_url='login')
def home_page(request):
    # получение текущего года и месяца
    curr_year = str(datetime.now().year)
    curr_month = str(datetime.now().month)
    # получение предыдущего месяца
    if datetime.now().month != 1:
        previous_month = str(datetime.now().month - 1)
        previous_year = curr_year
    else:
        previous_month = '12'
        previous_year = str(datetime.now().year - 1)


    # вывод total'ов в текущем месяце
    total_incomes = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                type='Income').aggregate(Sum("amount"))['amount__sum']
    total_outcomes = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                type='Outcome').aggregate(Sum("amount"))['amount__sum']
    total_investments = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                type='Investment').aggregate(Sum("amount"))['amount__sum']
    # инвестировано за все время
    all_time_investments = Transactions.objects.filter(type='Investment').aggregate(Sum("amount"))['amount__sum']

    # динамика к предыдущему месяцу
    total_incomes_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                type='Income').aggregate(Sum("amount"))['amount__sum']
    incomes_perc = round((total_incomes - total_incomes_prev) * 100 / total_incomes_prev, 1)

    total_outcomes_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                type='Outcome').aggregate(Sum("amount"))['amount__sum']
    outcomes_perc = round((total_outcomes - total_outcomes_prev) * 100 / total_outcomes_prev, 1)

    total_investments_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                type='Investment').aggregate(Sum("amount"))['amount__sum']
    investments_perc = round((total_investments - total_investments_prev) * 100 / total_investments_prev, 1)

    # bar chart
    # работа с датами
    dates_list = Transactions.objects.values_list('date')
    min_date = dates_list.order_by('date').first()[0]
    max_date = dates_list.order_by('date').last()[0]
    min_date_str = dates_list.filter(date__year=curr_year, date__month=curr_month).order_by('date').first()[0].strftime(
        "%Y-%m-%d")
    max_date_str = dates_list.filter(date__year=curr_year, date__month=curr_month).order_by('date').last()[0].strftime(
        "%Y-%m-%d")

    # работа с транзакциями
    transaction = Transactions.objects.filter(~Q(type='Investment')).values('date', 'type').order_by().annotate(amount=Sum('amount')).order_by('date')
    transaction = list(transaction)
    # приведение дат к строке
    for item in transaction:
        item['date'] = item['date'].strftime("%Y-%m-%d")

    # заполнение пропущенных дат нулями
    all_dates_list = pd.date_range(min_date, max_date).strftime("%Y-%m-%d").to_list()

    for el in all_dates_list:
        transaction.append({'date': el, 'type': 'Income', 'amount': 0})
        transaction.append({'date': el, 'type': 'Outcome', 'amount': 0})

    transaction_json = json.dumps(transaction)
    transaction_df = pd.read_json(transaction_json)
    transaction_df['date'] = transaction_df['date'].dt.strftime("%Y-%m-%d")

    # группировка датафрейма
    transaction_df = transaction_df.groupby(['date', 'type'], as_index=False).agg(
        sum_of_amount=('amount', 'sum')).sort_values(by='date')
    transaction_json = transaction_df.to_json(orient='records')
    transaction = json.loads(transaction_json)
    return render(request, 'home/index.html', {'transaction': transaction,
                                               'min_date': min_date_str,
                                               'max_date': max_date_str,
                                               'total_incomes': total_incomes,
                                               'total_outcomes': total_outcomes,
                                               'total_investments': total_investments,
                                               'all_time_investments': all_time_investments,
                                               'incomes_perc': incomes_perc,
                                               'outcomes_perc': outcomes_perc,
                                               'investments_perc': investments_perc})

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

    # работа со временем
    curr_year = str(datetime.now().year)
    curr_month = str(datetime.now().month)

    # bar chart
        # работа с датами
    dates_list = Transactions.objects.values_list('date')
    min_date = dates_list.order_by('date').first()[0]
    max_date = dates_list.order_by('date').last()[0]
    min_date_str = dates_list.filter(date__year=curr_year, date__month=curr_month).order_by('date').first()[0].strftime("%Y-%m-%d")
    max_date_str = dates_list.filter(date__year=curr_year, date__month=curr_month).order_by('date').last()[0].strftime("%Y-%m-%d")

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

    # doughnut chart
    doughnut = Transactions.objects.filter(date__year=curr_year, date__month=curr_month).values('type', 'category').order_by().annotate(sum_of_amount=Sum('amount')).order_by('-sum_of_amount')
    # данные для сводки по категориям
    by_category = Transactions.objects.filter(date__year=curr_year,
                                              date__month=curr_month).values('type', 'category') \
                                      .order_by().annotate(sum_of_amount=Sum('amount'),
                                                           count=Count('amount')).order_by('-sum_of_amount')
    # данные по total метрикке
    total = Transactions.objects.filter(date__year=curr_year,
                                              date__month=curr_month).values('type') \
                                      .order_by().annotate(sum_of_amount=Sum('amount'))

    # получение предыдущего месяца
    if datetime.now().month != 1:
        previous_month = str(datetime.now().month - 1)
        previous_year = curr_year
    else:
        previous_month = '12'
        previous_year = str(datetime.now().year - 1)

    # total в текущем месяце
    total_incomes = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                type='Income').aggregate(Sum("amount"))['amount__sum']
    total_outcomes = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                 type='Outcome').aggregate(Sum("amount"))['amount__sum']
    total_investments = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                    type='Investment').aggregate(Sum("amount"))['amount__sum']

    # динамика к предыдущему месяцу
    total_incomes_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                     type='Income').aggregate(Sum("amount"))['amount__sum']
    incomes_perc = round((total_incomes - total_incomes_prev) * 100 / total_incomes_prev, 1)

    total_outcomes_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                      type='Outcome').aggregate(Sum("amount"))['amount__sum']
    outcomes_perc = round((total_outcomes - total_outcomes_prev) * 100 / total_outcomes_prev, 1)

    total_investments_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                         type='Investment').aggregate(Sum("amount"))['amount__sum']
    investments_perc = round((total_investments - total_investments_prev) * 100 / total_investments_prev, 1)

    all_type_perc = [{'type': 'Income', 'perc': str(incomes_perc)},
                     {'type': 'Outcome', 'perc': str(outcomes_perc)},
                     {'type': 'Investment', 'perc': str(investments_perc)}]

    return render(request, 'home/statistics.html', {'transaction': transaction, 'min_date': min_date_str,
                                                    'max_date': max_date_str, 'doughnut': doughnut,
                                                    'by_category': by_category, 'total': total,
                                                    'all_type_perc': all_type_perc})


def history(request):
    return render(request, 'home/history.html')

def profile(request):
    error=''
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            error = 'error'
    form = ProfileForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'home/profile.html', data)

def create(request):
    error=''
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            error = 'error'
    form = ProfileForm()

    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'home/profile.html', data)