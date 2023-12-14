from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=70, verbose_name='Наименование')

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=70, verbose_name='Наименование')

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, null=True, verbose_name='Полное описание')
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey('webapp.Type', on_delete=models.PROTECT, verbose_name='Тип')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    edit_time = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return self.title
