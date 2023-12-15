from django import forms
from .models import Status, Type, Task


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': 'Наименование'}


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        labels = {'name': 'Наименование'}


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'types']
        labels = {
            'title': 'Заголовок',
            'description': 'Полное описание',
            'status': 'Статус',
            'types': 'Типы'
        }
