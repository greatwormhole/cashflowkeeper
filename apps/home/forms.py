from .models import Transactions, Category, Profile
from django.forms import ModelForm, TextInput, DateInput, Textarea, NumberInput, Select

choices = Category.objects.all().values_list('category', 'category')

choice_list = []

for item in choices:
    choice_list.append(item)


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

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'country']

        widgets = {
            "first_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'name'
            }),
            "last_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'surname'
            }),
            "country": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'country'
            }),
        }
