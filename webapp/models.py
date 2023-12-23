from django.db import models
from .validators import validate_title, validate_description


class Status(models.Model):
    name = models.CharField(max_length=70, verbose_name='Наименование')

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=70, verbose_name='Наименование')

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', validators=[validate_title])
    description = models.TextField(blank=True, null=True, verbose_name='Полное описание',
                                   validators=[validate_description])
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, verbose_name='Статус')
    types = models.ManyToManyField('webapp.Type', blank=True, related_name='tasks', verbose_name='Типы')
    project = models.ForeignKey('webapp.Project', on_delete=models.PROTECT, verbose_name='Проект')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    edit_time = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return self.title


class Project(models.Model):
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата окончания')
    name = models.CharField(max_length=70, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name
