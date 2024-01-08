from django import forms
from django.contrib.auth import get_user_model
from .models import Status, Type, Task, Project


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
            'types': 'Типы',
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['start_date', 'end_date', 'name', 'description', 'authors']
        labels = {
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'name': 'Наименование',
            'description': 'Описание',
            'authors': 'Авторы',
        }


class ProjectSearchForm(forms.Form):
    q = forms.CharField(label='Поиск', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


class ProjectUserForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Выберите пользователей',
    )

    class Meta:
        model = Project
        fields = ['authors']
