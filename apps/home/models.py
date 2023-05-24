from django.db import models
from django.contrib.auth.models import User

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    title = models.CharField('Название', max_length = 50)
    amount = models.PositiveIntegerField('Сумма транзакции')
    created = models.DateTimeField('Дата транзакции')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Добавление"
        verbose_name_plural = "Добавления"

class History(models.Model):
    title = models.CharField('Название', max_length=50)
    amount = models.PositiveIntegerField('Сумма транзакции')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Добавление"
        verbose_name_plural = "Добавления"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    title = models.CharField('Название', max_length=50)
    amount = models.PositiveIntegerField('Сумма транзакции')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Добавление"
        verbose_name_plural = "Добавления"

class Statistics(models.Model):
    title = models.CharField('Название', max_length=50)
    amount = models.PositiveIntegerField('Сумма транзакции')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Добавление"
        verbose_name_plural = "Добавления"