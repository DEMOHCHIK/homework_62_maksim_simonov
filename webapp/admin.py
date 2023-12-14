from django.contrib import admin
from .models import Status, Type, Task


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'type', 'add_time', 'edit_time']
