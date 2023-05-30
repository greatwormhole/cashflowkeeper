from .models import Transactions, Category
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, NumberInput, Select

choices = Category.objects.all().values_list('category', 'category')

choice_list = []

for item in choices:
    choice_list.append(item)


type_choices = [('income', 'income'), ('outcome', 'outcome'), ('investment', 'investment')]

class TransactionsForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['date', 'category', 'amount', 'comment', 'profile', 'type']

        widgets = {
            "profile": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Профиль'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата расхода'
            }),
            "category": Select(choices=choice_list, attrs={
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