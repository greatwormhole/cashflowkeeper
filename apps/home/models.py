from django.db import models

class Additions(models.Model):
    title = models.CharField('Название', max_length=50)

    class Meta:
        verbose_name = "Добавление"
        verbose_name_plural = "Добавления"

class History(models.Model):
    pass

class Profile(models.Model):
    pass

class Statistics(models.Model):
    pass