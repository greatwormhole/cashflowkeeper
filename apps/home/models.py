from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField()
#
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователя"


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Transactions(models.Model):

    date = models.DateTimeField('Дата транзакции')
    category = models.CharField(max_length=255, default='other')
    amount = models.PositiveIntegerField('Сумма транзакции')
    comment = models.CharField('Комментарий', max_length=50)
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='income')

    def __str__(self):
        return f"{self.date} {self.amount}"

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"







