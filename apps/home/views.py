from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transactions, Category
from .forms import TransactionsForm, EditForm, CalendarForm
from django.db.models import Sum, Q, Count
import pandas as pd
import datetime
from datetime import date, timedelta, datetime
import json
import numpy as np
from django.views.generic import TemplateView
from .charts import objects_to_df, Chart
from django import forms

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

    if Transactions.objects.all().filter(date__year=curr_year, date__month=curr_month,
                                         type='Income').count() != 0:
        total_incomes = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                    type='Income').aggregate(Sum("amount"))['amount__sum']
    else:
        total_incomes = 0

    if Transactions.objects.all().filter(date__year=curr_year, date__month=curr_month,
                                         type='Outcome').count() != 0:
        total_outcomes = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                     type='Outcome').aggregate(Sum("amount"))['amount__sum']
    else:
        total_outcomes = 0

    if Transactions.objects.all().filter(date__year=curr_year, date__month=curr_month,
                                         type='Investment').count() != 0:
        total_investments = Transactions.objects.filter(date__year=curr_year, date__month=curr_month,
                                                        type='Investment').aggregate(Sum("amount"))['amount__sum']
    else:
        total_investments = 0

        # инвестировано за все время
    if Transactions.objects.all().filter(type='Investment').count() != 0:
        all_time_investments = Transactions.objects.filter(type='Investment').aggregate(Sum("amount"))['amount__sum']
    else:
        all_time_investments = 0

    # динамика к предыдущему месяцу
    if Transactions.objects.all().filter(date__year=previous_year, date__month=previous_month,
                                         type='Income').count() != 0:
        total_incomes_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                         type='Income').aggregate(Sum("amount"))['amount__sum']
        incomes_perc = round((total_incomes - total_incomes_prev) * 100 / total_incomes_prev, 1)
    else:
        incomes_perc = 0

    if Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                   type='Outcome').all().count() != 0:
        total_outcomes_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                          type='Outcome').aggregate(Sum("amount"))['amount__sum']
        outcomes_perc = round((total_outcomes - total_outcomes_prev) * 100 / total_outcomes_prev, 1)
    else:
        outcomes_perc = 0

    if Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                   type='Investment').all().count() != 0:
        total_investments_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                             type='Investment').aggregate(Sum("amount"))['amount__sum']
        investments_perc = round((total_investments - total_investments_prev) * 100 / total_investments_prev, 1)
    else:
        investments_perc = 0

    # bar chart
    # работа с датами
    dates_list = Transactions.objects.values_list('date')
    if dates_list.all().count() != 0:
        min_date = dates_list.order_by('date').first()[0]
        max_date = dates_list.order_by('date').last()[0]
        min_date_str = dates_list.filter(date__year=curr_year, date__month=curr_month).order_by('date').first()[
            0].strftime(
            "%Y-%m-%d")
        max_date_str: object = dates_list.filter(date__year=curr_year, date__month=curr_month).order_by('date').last()[
            0].strftime(
            "%Y-%m-%d")
    else:
        min_date = '2023-01-01'
        max_date = '2023-01-01'
        min_date_str = '2023-01-01'
        max_date_str = '2023-01-31'

    # работа с транзакциями
    transaction = Transactions.objects.filter(~Q(type='Investment')).values('date', 'type').order_by().annotate(
        amount=Sum('amount')).order_by('date')
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
    return render(request, 'home/HomePage.html', {'transaction': transaction,
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
    return render(request, 'home/Add.html', data)


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

    if dates_list.all().count() != 0:
        min_date = dates_list.order_by('date').first()[0]
        max_date = dates_list.order_by('date').last()[0]
        min_date_str = dates_list.filter(date__year=curr_year, date__month=curr_month).order_by('date').first()[
            0].strftime(
            "%Y-%m-%d")
        max_date_str: object = dates_list.filter(date__year=curr_year, date__month=curr_month).order_by('date').last()[
            0].strftime(
            "%Y-%m-%d")
    else:
        min_date = '2023-01-01'
        max_date = '2023-01-01'
        min_date_str = '2023-01-01'
        max_date_str = '2023-01-31'

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
    transaction_df = transaction_df.groupby(['date', 'type'], as_index=False).agg(
        sum_of_amount=('amount', 'sum')).sort_values(by='date')
    transaction_json = transaction_df.to_json(orient='records')
    transaction = json.loads(transaction_json)

    # doughnut chart
    doughnut = Transactions.objects.filter(date__year=curr_year, date__month=curr_month).values('type',
                                                                                                'category').order_by().annotate(
        sum_of_amount=Sum('amount')).order_by('-sum_of_amount')
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
    if Transactions.objects.all().filter(date__year=previous_year, date__month=previous_month,
                                         type='Income').count() != 0:
        total_incomes_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                         type='Income').aggregate(Sum("amount"))['amount__sum']
        incomes_perc = round((total_incomes - total_incomes_prev) * 100 / total_incomes_prev, 1)
    else:
        incomes_perc = 0

    if Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                   type='Outcome').all().count() != 0:
        total_outcomes_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                          type='Outcome').aggregate(Sum("amount"))['amount__sum']
        outcomes_perc = round((total_outcomes - total_outcomes_prev) * 100 / total_outcomes_prev, 1)
    else:
        outcomes_perc = 0

    if Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                   type='Investment').all().count() != 0:
        total_investments_prev = Transactions.objects.filter(date__year=previous_year, date__month=previous_month,
                                                             type='Investment').aggregate(Sum("amount"))['amount__sum']
        investments_perc = round((total_investments - total_investments_prev) * 100 / total_investments_prev, 1)
    else:
        investments_perc = 0
    all_type_perc = [{'type': 'Income', 'perc': str(incomes_perc)},
                     {'type': 'Outcome', 'perc': str(outcomes_perc)},
                     {'type': 'Investment', 'perc': str(investments_perc)}]

    return render(request, 'home/statistics_old.html', {'transaction': transaction, 'min_date': min_date_str,
                                                        'max_date': max_date_str, 'doughnut': doughnut,
                                                        'by_category': by_category, 'total': total,
                                                        'all_type_perc': all_type_perc})


def history(request):
    return render(request, 'home/History.html')


def main(request):
    return render(request, 'home/MainPage.html')


def profile(request):
    error = ''
    data = {
        'data1': 1,
        'data2': 2,
    }
    return render(request, 'home/ProfileAndSetting.html', data)


def create(request):
    # error = ''
    # if request.method == 'POST':
    #     form = ProfileForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('profile')
    #     else:
    #         error = 'error'
    # form = ProfileForm()
    #
    # data = {
    #     'form': form,
    #     'error': error,
    # }
    return render(request, 'home/profile.html')



PALETTE = ['rgba(117, 223, 177, 1)', 'rgba(217, 94, 94, 1)']

class Statboard(TemplateView):
    template_name = 'home/statistics_new.html'

    end_date = date.today().strftime('%Y-%m-%d')
    start_date = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')

    current_type = 'Income'


    def get(self, request, *args, **kwargs):
        if 'Income' in self.request.GET:
            context = super().get_context_data(**kwargs)

            end_date = self.end_date
            start_date = self.start_date


            df = objects_to_df(Transactions, date_cols=['%Y-%m-%d', 'date'])
            df = df[(df['type'] == "Income") & (df['date'] >= start_date) & (df['date'] <= end_date)]
            context['charts'] = []

            one_side_bar = Chart('bar', chart_id='one_side_bar', palette='rgba(31, 180, 171, 1)')
            one_side_bar.from_df(df, values='amount', labels=['date'])

            doughnut = Chart('doughnut', chart_id='doughnut', palette=PALETTE)
            doughnut.from_df(df, values='amount', labels=['category'])

            context['charts'].append(one_side_bar.get_presentation())
            context['charts'].append(doughnut.get_presentation())

            # Calendar = CalendarForm()
            # start_date_field = datetime.strptime(start_date, '%Y-%m-%d').date()
            # end_date_field = datetime.strptime(end_date, '%Y-%m-%d').date()
            # Calendar.change_date_field(forms.DateField(widget=forms.SelectDateWidget, initial=start_date_field),
            #                            forms.DateField(widget=forms.SelectDateWidget, initial=end_date_field))
            # Calendar.start_date_field = forms.DateField(widget=forms.SelectDateWidget, initial=start_date_field)
            # Calendar.end_date_field = forms.DateField(widget=forms.SelectDateWidget, initial=end_date_field)
            context['date'] = CalendarForm()

            # total amount
            total = df['amount'].sum()
            context['total'] = total

            # change current page
            self.change_type("Income")

            # by category
            by_category_df = df.groupby('category', as_index=False).agg({'id': 'count', 'amount': 'sum'})
            by_category_json = by_category_df.to_json(orient='records')
            by_category = json.loads(by_category_json)
            context['by_category'] = by_category

            return render(request, self.template_name, context)

        elif 'Outcome' in self.request.GET:
            context = super().get_context_data(**kwargs)

            end_date = self.end_date
            start_date = self.start_date

            df = objects_to_df(Transactions, date_cols=['%Y-%m-%d', 'date'])
            df = df[(df['type'] == "Outcome") & (df['date'] >= start_date) & (df['date'] <= end_date)]

            context['charts'] = []

            one_side_bar = Chart('bar', chart_id='one_side_bar', palette='rgba(31, 180, 171, 1)')
            one_side_bar.from_df(df, values='amount', labels=['date'])

            doughnut = Chart('doughnut', chart_id='doughnut', palette=PALETTE)
            doughnut.from_df(df, values='amount', labels=['category'])

            context['charts'].append(one_side_bar.get_presentation())
            context['charts'].append(doughnut.get_presentation())

            context['date'] = CalendarForm()

            # total amount
            total = df['amount'].sum()
            context['total'] = total

            # change current page
            self.change_type("Outcome")

            # by category
            by_category_df = df.groupby('category', as_index=False).agg({'id': 'count', 'amount': 'sum'})
            by_category_json = by_category_df.to_json(orient='records')
            by_category = json.loads(by_category_json)
            context['by_category'] = by_category

            return render(request, self.template_name, context)

        elif 'Investment' in self.request.GET:
            context = super().get_context_data(**kwargs)

            end_date = self.end_date
            start_date = self.start_date

            df = objects_to_df(Transactions, date_cols=['%Y-%m-%d', 'date'])
            df = df[(df['type'] == "Investment") & (df['date'] >= start_date) & (df['date'] <= end_date)]

            context['charts'] = []

            one_side_bar = Chart('bar', chart_id='one_side_bar', palette='rgba(31, 180, 171, 1)')
            one_side_bar.from_df(df, values='amount', labels=['date'])

            doughnut = Chart('doughnut', chart_id='doughnut', palette=PALETTE)
            doughnut.from_df(df, values='amount', labels=['category'])

            context['charts'].append(one_side_bar.get_presentation())
            context['charts'].append(doughnut.get_presentation())

            context['date'] = CalendarForm()

            # total amount
            total = df['amount'].sum()
            context['total'] = total

            # change current page
            self.change_type("Investment")

            # by category
            by_category_df = df.groupby('category', as_index=False).agg({'id': 'count', 'amount': 'sum'})
            by_category_json = by_category_df.to_json(orient='records')
            by_category = json.loads(by_category_json)
            context['by_category'] = by_category

            return render(request, self.template_name, context)

        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        all_data = request.POST
        start_day = all_data.getlist('start_date_field_day')[0]
        start_month = all_data.getlist('start_date_field_month')[0]
        start_year = all_data.getlist('start_date_field_year')[0]
        end_day = all_data.getlist('end_date_field_day')[0]
        end_month = all_data.getlist('end_date_field_month')[0]
        end_year = all_data.getlist('end_date_field_year')[0]
        start_date = datetime.strptime(f'{start_year}-{start_month}-{start_day}', '%Y-%m-%d').date().strftime('%Y-%m-%d')
        end_date = datetime.strptime(f'{end_year}-{end_month}-{end_day}', '%Y-%m-%d').date().strftime('%Y-%m-%d')

        self.change_date(start_date, end_date)

        temp_dict = self.request.GET.copy()
        type = self.current_type
        temp_dict[type] = type
        self.request.GET = temp_dict

        return self.get(request, *args, **kwargs)

    @classmethod
    def change_date(cls, start_date, end_date):
        cls.start_date = start_date
        cls.end_date = end_date

    @classmethod
    def change_type(cls, type):
        cls.current_type = type


class Homeboard(TemplateView):
    template_name = 'home/homepage_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        df = objects_to_df(Transactions, date_cols=['%Y-%m, %B', 'date'])
        df = df.query('type in ("Income", "Outcome")').groupby(['date', 'type'], as_index=False).agg({'amount': 'sum'})
        context['charts'] = []
        multi_side_bar = Chart('bar', chart_id='multi_side_bar', palette=PALETTE)
        multi_side_bar.from_df(df, values='amount', labels=['date'], stacks='type')

        context['charts'].append(multi_side_bar.get_presentation())

        # total amount by current month
        df_2 = objects_to_df(Transactions, date_cols=['%Y-%m, %B', 'date']).groupby(['date', 'type'], as_index=False).agg({'amount': 'sum'})
        current_month = date.today().strftime('%Y-%m, %B')
        total_by_type_df = df_2.query('date == @current_month')
        total_by_type_json = total_by_type_df.to_json(orient='records')
        total_by_type = json.loads(total_by_type_json)
        context['total_by_type'] = total_by_type

        # increase compared to the previous month
        today = date.today()
        if today.month == 1:
            previous_month = today.replace(year=today.year - 1, month=12)
        else:
            previous_month = today.replace(month=today.month - 1)
        previous_month = previous_month.strftime('%Y-%m, %B')
        total_by_type_df_previous = df_2.query('date == @previous_month')

        try:
            increase_income = (total_by_type_df.query('type == "Income"')['amount'].values[0] -
                               total_by_type_df_previous.query('type == "Income"')['amount'].values[0]) * 100 / total_by_type_df_previous.query('type == "Income"')['amount'].values[0]
            increase_income = round(increase_income, 1)
        except:
            increase_income = 0

        try:
            increase_outcome = (total_by_type_df.query('type == "Outcome"')['amount'].values[0] -
                               total_by_type_df_previous.query('type == "Outcome"')['amount'].values[0]) * 100 / total_by_type_df_previous.query('type == "Outcome"')['amount'].values[0]
            increase_outcome = round(increase_outcome, 1)
        except:
            increase_outcome = 0

        try:
            increase_investment = (total_by_type_df.query('type == "Investment"')['amount'].values[0] -
                               total_by_type_df_previous.query('type == "Investment"')['amount'].values[0]) * 100 / total_by_type_df_previous.query('type == "Investment"')['amount'].values[0]
            increase_investment = round(increase_investment, 1)
        except:
            increase_investment = 0

        context['increase_income'] = increase_income
        context['increase_outcome'] = increase_outcome
        context['increase_investment'] = increase_investment

        return context