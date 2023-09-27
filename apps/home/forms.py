from .models import Transactions, Category
from django.forms import ModelForm, TextInput, DateInput, Textarea, NumberInput, Select, DateField
from django import forms
from django.contrib.admin import widgets
from datetime import date, timedelta, datetime
# choices = Category.objects.all().values_list('category', 'category')

# choice_list = []

# for item in choices:
#     choice_list.append(item)


type_choices = [('Income', 'Income'), ('Outcome', 'Outcome'), ('Investment', 'Investment')]

class TransactionsForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['date', 'category', 'amount', 'comment', 'profile', 'type']

        widgets = {
            "profile": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Профиль'
            }),
            "date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата расхода'
            }),
            "category": Select(choices='choice_list', attrs={
                'class': 'form-control',
                'placeholder': 'Выбеите категорию'
            }),
            "amount": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма'
            }),
            "comment": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий'
            }),
            "type": Select(choices=type_choices, attrs={
                'class': 'form-control',
                'placeholder': 'Тип операции'
            })
        }

class EditForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category']

        widgets = {
            "category": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Добавьте категорию'
            }),
        }

class CalendarForm(forms.Form):

    start_date_field = forms.DateField(widget=forms.SelectDateWidget, initial=(date.today() - timedelta(days=7)))
    end_date_field = forms.DateField(widget=forms.SelectDateWidget, initial=date.today())

    # @classmethod
    # def change_date_field(cls, start_date_field, end_date_field):
    #     cls.start_date_field = start_date_field
    #     cls.end_date_field = end_date_field

